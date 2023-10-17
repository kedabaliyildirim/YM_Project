# Check if a comment is provided as an argument
if ($args.Count -eq 0) {
    Write-Error "Please provide a comment for the commit."
    return
}

# Save all requirements to a requirements.txt file
pip freeze > requirements.txt

# Add, commit and push the requirements.txt file to GitHub with the provided comment
git add .
git commit -m $args[0]
git push
