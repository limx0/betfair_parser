# betfair_parser

A simple and fast betfair parser, built with [msgspec](https://github.com/jcrist/msgspec).

### Releasing

Releases are published automatically when a tag is pushed to GitHub.

```
# Set next version number
export RELEASE=x.x.x

# Create tags
git commit --allow-empty -m "Release $RELEASE"
git tag -a $RELEASE -m "Version $RELEASE"

# Push
git push upstream --tags
```