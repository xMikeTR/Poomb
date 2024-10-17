<h1>
  Poomb
</h1>

<div align="center">
  <br />
  <a href="#about"><strong>Explore the screenshots »</strong></a>
  <br />
  <br />
  <a href="https://github.com/xMikeTR/poomb/issues/new?assignees=&labels=bug&template=01_BUG_REPORT.md&title=bug%3A+">Report a Bug</a>
  ·
  <a href="https://github.com/xMikeTR/poomb/issues/new?assignees=&labels=enhancement&template=02_FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>
  .
  <a href="https://github.com/xMikeTR/poomb/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+">Ask a Question</a>
</div>

<div align="center">
<br />

[![Project license](https://img.shields.io/github/license/xMikeTR/poomb.svg?style=flat-square)](LICENSE)

[![Pull Requests welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg?style=flat-square)](https://github.com/xMikeTR/poomb/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
[![code with love by xMikeTR](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-xMikeTR-ff1414.svg?style=flat-square)](https://github.com/xMikeTR)

</div>

<details open="open">
<summary>Table of Contents</summary>

- [About](#about)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Support](#support)
- [Project assistance](#project-assistance)
- [Contributing](#contributing)
- [Authors & contributors](#authors--contributors)
- [Security](#security)
- [License](#license)
- [Acknowledgements](#acknowledgements)

</details>

---

## About
#### Video Demo:  <https://youtu.be/xFlV1g4JAkU>

> Poomb is a webapp tailored for weightlifters.
> It allows you to track and analyze your performance, workout by workout,
> In so doing through visualizations so you can truly see your progress
> This was done so we can have better control of our targets.

To achieve this, various features were created, from your basic CRUD functions that allow you to insert, update and update your training log listed in log.py,
the file also contains functions for the password reset, and displaying your overall performance.

To protect users and have general security, auth.py was created, it is responsible for authorization functions, not allowing one to see other user's information

Stored as displayed in db.py

To assist with this functionality, api.py was created to grab information from the database itself, this was done due to the views returning information, this was so we could return from the database.
Also useful to this would be any events that occurred and you'd like to be updated, that's where webscrape.py comes in.
By using beautiful soup and asyncio, this grabs information from the powerlifting website and displays according to user country.


As another helper file, emails.py and keygen,py were created for the password reset functions respectively


<details>
<summary>Screenshots</summary>
<br>



|                               Home Page                               |                               Login Page                               |
| :-------------------------------------------------------------------: | :--------------------------------------------------------------------: |
| <img src="/home/mike/Pictures/Screenshots/home.png" title="Home Page" width="100%"> | <img src="docs/images/screenshot.png" title="Login Page" width="100%"> |

</details>

### Built With


> Flask
> ChartJS

## Getting Started

### Prerequisites


> If any mod is to be done, please setup your virtual environment with venv.

### Installation


> In order to install, after cloning the repo, pip install -r requirements.txt should allow you to install all the necessary libraries



## Roadmap

See the [open issues](https://github.com/xMikeTR/poomb/issues) for a list of proposed features (and known issues).

- [Top Feature Requests](https://github.com/xMikeTR/poomb/issues?q=label%3Aenhancement+is%3Aopen+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Top Bugs](https://github.com/xMikeTR/poomb/issues?q=is%3Aissue+is%3Aopen+label%3Abug+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Newest Bugs](https://github.com/xMikeTR/poomb/issues?q=is%3Aopen+is%3Aissue+label%3Abug)

## Support

> miketr1990@gmail.com

Reach out to the maintainer at one of the following places:

- [GitHub issues](https://github.com/xMikeTR/poomb/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+)
- Contact options listed on [this GitHub profile](https://github.com/xMikeTR)

## Project assistance

If you want to say **thank you** or/and support active development of Poomb:

- Add a [GitHub Star](https://github.com/xMikeTR/poomb) to the project.
- Tweet about the Poomb.
- Write interesting articles about the project on [Dev.to](https://dev.to/), [Medium](https://medium.com/) or your personal blog.

Together, we can make Poomb **better**!

## Contributing

First off, thanks for taking the time to contribute! Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make will benefit everybody else and are **greatly appreciated**.


Please read [our contribution guidelines](docs/CONTRIBUTING.md), and thank you for being involved!

## Authors & contributors

The original setup of this repository is by [Miguel Fialho](https://github.com/xMikeTR).

For a full list of all authors and contributors, see [the contributors page](https://github.com/xMikeTR/poomb/contributors).

## Security

Poomb follows good practices of security, but 100% security cannot be assured.
Poomb is provided **"as is"** without any **warranty**. Use at your own risk.

_For more information and to report security issues, please refer to our [security documentation](docs/SECURITY.md)._

## License

This project is licensed under the **MIT license**.

See [LICENSE](LICENSE) for more information.

## Acknowledgements

> CS50 Course for inspiring this project
