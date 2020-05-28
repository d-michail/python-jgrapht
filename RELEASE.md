
# Release

 1. Open `jgrapht/__version__.py` and change version from `<backendversion>.<minor>dev` to 
    `<backendversion>.<minor>` or `<backendversion>.<minor>rc1` if you are going for a 
    release candidate.

 2. Make sure docs are correctly generated. Use `cd docs && make html` and inspect the 
    output.

 3. Commit changes
    `git commit -m "X.X release"`

 4. Add the version number as a tag in git::

    git tag -s [-u <key-id>] jgrapht-<backendversion>.<minor> -m 'signed <backendversion>.<minor> tag'

    (If you do not have a gpg key, use -m instead; it is important for
    Debian packaging that the tags are annotated)

 5. Push the new meta-data to github::

    git push --tags upstream master

    (where ``upstream`` is the name of the
    ``github.com:d-michail/python-jgrapht`` repository.)

 6. PyPi packages will be uploaded by travis

 7. Wait until readthedocs updates the documentation.

 8. Increase the version number in `jgrapht/__version__.py` and add a `dev` suffix

 9. Commit and push changes::

    git add jgrapht/__version__.py
    git commit -m "Bump release version"
    git push upstream master

 10. Done

