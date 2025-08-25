1. Never use — (em dashes). Try to structure sentences to these are not needed.
2. For markdown formatting, use: `nix-shell -p nodePackages.prettier --run "find . -name '*.md' -not -path './.git/*' -print0 | xargs -0 prettier --parser=markdown --write"`
3. Or run the script: `./format-markdown.sh`
4. Always add a new line in the end of files
