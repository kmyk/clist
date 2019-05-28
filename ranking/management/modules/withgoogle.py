#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import REQ, BaseModule
from excepts import ExceptionParseStandings

from concurrent.futures import ThreadPoolExecutor as PoolExecutor

import base64
import re
import json
import tqdm
from datetime import datetime


class Statistic(BaseModule):
    API_RANKING_URL_FORMAT_ = 'https://codejam.googleapis.com/scoreboard/{id}/poll?p='

    def __init__(self, **kwargs):
        super(Statistic, self).__init__(**kwargs)

    def get_standings(self, users=None):
        match = re.search('/([0-9a-f]{16})$', self.url)
        if not match:
            raise ExceptionParseStandings(f'Not found id in url = {self.url}')
        self.id = match.group(1)
        standings_url = self.url

        api_ranking_url_format = self.API_RANKING_URL_FORMAT_.format(**self.__dict__)

        def get(offset, num):
            query = f'{{"min_rank":{offset},"num_consecutive_users":{num}}}'
            base64_query = base64.b64encode(query.encode())
            url = api_ranking_url_format + base64_query.decode()
            content = REQ.get(url)
            content = content.replace(b'-', b'+')
            content = content.replace(b'_', b'/')
            content = re.sub(rb'[^A-Za-z0-9\+\/]', b'', content)
            content += b'=' * ((4 - len(content) % 4) % 4)
            data = json.loads(base64.b64decode(content).decode())
            return data

        data = get(1, 1)

        num_consecutive_users = 200
        n_page = (data['full_scoreboard_size'] - 1) // num_consecutive_users + 1

        def fetch_page(page):
            return get(page * num_consecutive_users + 1, num_consecutive_users)

        result = {}
        with PoolExecutor(max_workers=8) as executor:
            for data in tqdm.tqdm(executor.map(fetch_page, range(n_page)), total=n_page):
                problem_infos = {d['id']: d for d in data['challenge']['tasks']}
                for row in data['user_scores']:
                    if not row['task_info']:
                        continue
                    handle = row.pop('displayname')

                    r = result.setdefault(handle, {})
                    r['member'] = handle
                    r['place'] = row.pop('rank')
                    r['solving'] = row.pop('score_1')
                    r['penalty'] = self.to_time(-row.pop('score_2') / 10**6)

                    solved = 0
                    problems = r.setdefault('problems', {})
                    for task_info in row['task_info']:
                        problem_info = problem_infos[task_info['task_id']]
                        full_score = sum([t['value'] for t in problem_info['tests']])

                        p = problems.setdefault(problem_info['title'], {})
                        p['time'] = self.to_time(task_info['penalty_micros'] / 10**6)
                        p['result'] = task_info['score']
                        if p['result'] and p['result'] != full_score:
                            p['partial'] = True
                        if task_info['penalty_attempts']:
                            p['penalty'] = task_info['penalty_attempts']
                        solved += task_info['tests_definitely_solved']
                    r['solved'] = {'solving': solved}

        standings = {
            'result': result,
            'url': standings_url,
        }
        return standings


if __name__ == "__main__":
    from pprint import pprint
    statictic = Statistic(
        name='Round 2 2019',
        url='https://codingcompetitions.withgoogle.com/codejam/round/0000000000051679',
        key='0d4dvct96b7cpf0tml4elq0n9r',
        start_time=datetime.now(),
        standings_url=None,
    )
    # pprint(statictic.get_standings())
    statictic = Statistic(
        name='Round B 2019',
        url='https://codingcompetitions.withgoogle.com/kickstart/round/0000000000050eda',
        key='0d4dvct96b7cpf0tml4elq0n9r',
        start_time=datetime.now(),
        standings_url=None,
    )
    pprint(statictic.get_standings())
