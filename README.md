`octofairy` is a machine learning based GitHub bot that, given certain features of an Issue, will try to predict if it'll ever be closed and if so, if with a commit or not.

**WORK IN PROGRESS**

Install [ergo](https://github.com/evilsocket/ergo) and then the deps of this project:

    make requirements

Set your GitHub API key and download issues as JSON files from a given repo:

    make download GITHUB_API_KEY="set-your-api-key-here" GITHUB_REPO=github.com/golang/go

Perform features extraction from the GitHub issues and vectorialize them:

    make convert GITHUB_REPO=github.com/golang/go

Train:

    make train GITHUB_REPO=github.com/golang/go

View the model:

    ergo view .
