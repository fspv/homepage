#!/bin/bash

# Format markdown files using Prettier via nix-shell
nix-shell -p nodePackages.prettier --run "
  find . -name '*.md' -not -path './.git/*' -print0 | \
  xargs -0 prettier --parser=markdown --write
"