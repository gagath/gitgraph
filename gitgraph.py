import os
import datetime

import pygit2


def days_range(start, end):
    """Build a range of days from start to end."""
    delta = end - start
    a_day = datetime.timedelta(days=1)

    for i in range(abs(delta.days)):

        # We handle the case where the delta can be negative so we need to
        # decrease days insted of increasing.
        offset = i * a_day
        val = start + offset if delta.days > 0 else start - offset

        yield val


def compute_color(nb, m):
    """Compute the color of a cell.

    Args:
        nb: number of commits
        m: maximum number of commits

    Returns:
        string containing color code in HTML format, eg. "#1e6823"

    """

    if m > 0:
        ratio = nb / m
    else:
        ratio = 0

    if ratio > 0.75:
        color = '1e6823'
    elif ratio > 0.5:
        color = '44a340'
    elif ratio > 0.25:
        color = '8cc665'
    elif ratio > 0:
        color = 'd6e685'
    else:
        color = 'eee'

    return '#{}'.format(color)


def retrieve_repo_activity(repo):

    # Retrieve last commit from repo as start point for walk
    last = repo[repo.head.target]

    # Initialize data we are going to return
    nb_commits = 0
    per_day_commits = {}

    # Walks though all the repository's commits by time

    # TODO: this is time-dependant depending on current time ; maybe do not use
    # datetime anymore but just date instead since we don't care about time of
    # commit and current time of the day.
    previous_date = None
    for commit in repo.walk(last.id, pygit2.GIT_SORT_TIME):
        commit_date = datetime.datetime.fromtimestamp(commit.commit_time).date()
        today_date = datetime.date.today()

        delta = today_date - commit_date

        if delta.days not in per_day_commits:
            per_day_commits[delta.days] = {
                'date': commit_date,
                'commits': 0
            }

        per_day_commits[delta.days]['commits'] += 1
        nb_commits += 1
        previous_date = commit_date

    # We retrieve first and last commit date
    first = previous_date
    last = datetime.date.today()

    # We generate a list of all days since first commit and fill it with
    # retrieved data.
    continuous_days_commits = []

    # TODO: We stop a day before today but in the graph we mark the last day as
    # today; which is wrong.
    for day in days_range(first, last):
        delta = (last - day).days

        if delta in per_day_commits:
            commits = per_day_commits[delta]['commits']
        else:
            commits = 0

        continuous_days_commits.append({
            'date': day,
            'commits': commits
        })

    return {
        'per_day_commits': per_day_commits,
        'continuous_days_commits': reversed(continuous_days_commits),
        'nb_commits': nb_commits
    }


def draw_activity(days):

    weeks = 24
    days = list(reversed(days))[-(weeks*7):]

    box_height = 10
    box_width = 10
    max_commits = max([d['commits'] for d in days])
    spacing = 3
    vertical_boxes = 7

    height = int(box_height * (vertical_boxes + spacing))
    width = int((len(days) / vertical_boxes + 1) * (box_width + spacing))

    print(
        '<?xml version="1.0" encoding="utf-8" ?>'
        '<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}">'
        '<title>test</title>'.format(width, height)
    )

    for n, day in enumerate(days):
        x = int(n / vertical_boxes) * (10 + spacing)
        y = (n % vertical_boxes) * (10 + spacing)

        date = day['date']

        print(
            '<g>'
            '<rect x="{}" y="{}" width="10" height="10" style="fill:{};{}" />'
            '<title>{} {}</title>'
            '</g>'
            .format(
                x, y,
                compute_color(day['commits'], max_commits),
                "stroke-width:1px;stroke:red" if n == len(days) - 1 else "",
                date,
                '{} commits'.format(day['commits'])
            )
        )

    print('</svg>')


if __name__ == "__main__":

    path = os.getcwd()

    try:
        gitpath = pygit2.discover_repository(path)
    except KeyError:
        pass

    repo = pygit2.Repository(gitpath)

    data = retrieve_repo_activity(repo)['continuous_days_commits']

    # for k in data:
    #     print(k['date'], k['commits'])

    draw_activity([day for day in data])
