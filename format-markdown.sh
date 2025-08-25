#!/bin/bash

# Format markdown files using Prettier via nix-shell
nix-shell -p nodePackages.prettier --run "prettier --parser=markdown --write **/*.md"