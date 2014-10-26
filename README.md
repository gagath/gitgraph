# pygitgraph, a git graphs generator

What about generating fun graphs out of your git repositories? (Python 3)

## Description

Some git providers like Github provide beautiful graphs representing the
activity of your repository. However, users should not depend on a such service
in order to generate graphs and be able to run it on local/standalone git
repositories too.

This can even be useful if you use another git hoster like Bitbucket which does
not provide these kind of graphs on their service.

## Requirements

You will need to install the following C library before everything in order to
use the Python-based libgit2 bindings:

 * libgit2

Then, you will need to install the following Python dependency on your system
or (better) inside a virtualenv:

 * pygit2

## Notes

At this point, this program is able to generate a single type of git graphs,
but you can contribute to it and add other git graphs generators!

This program is a rewrite of an old prototype written in C.

## License

Gitgraph is brought to you under GNU Affero General Public License version 3.
For further informations, please read the provided COPYING file.
