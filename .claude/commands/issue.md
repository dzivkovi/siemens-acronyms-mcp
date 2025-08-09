**Model Preference**: Use the latest Claude 4 Opus model

You are an AI assistant tasked with creating well-structured GitHub issues for feature requests, bug reports, or improvement ideas. Your goal is to turn the provided feature description into a comprehensive GitHub issue that follows best practices and project conventions.

First, you will be given a feature description. Here it is:

<feature_description>
#$ARGUMENTS
</feature_description>

Always replace <TYPE> with one of: feat, fix, docs, chore (based on work category).
If analysis/0000/DESIGN.md does not exist, generate the stub shown in the repo and link it.

Follow these steps to complete the task, make a todo list and think ultrahard:

1. Research the repository:
    - Examine the repository's structure, existing issues, and documentation.
    - Look for any CONTRIBUTING.md, ISSUE_TEMPLATE.md, or similar files that might contain guidelines for creating issues.
    - Note the project's coding style, naming conventions, and any specific requirements for submitting issues.

2. Research best practices:
    - Search for current best practices in writing GitHub Issues, focusing on clarity, completeness, and actionability.
    - Look for examples of well-written issues in popular open-source projects for inspiration.

3. Present a plan:
    - Based on your research, outline a plan for creating the GitHub issue.
    - Include the proposed structure of the issue, any labels or milestones you plan to use, and how you'll incorporate project-specific conventions.
    - Present this plan in `<plan>` tags.

4. Create the GitHub issue:
    - Once the plan is approved, draft the GitHub issue content.
    - Include a clear title, detailed description, acceptance criteria, and any additional context or resources that would be helpful for developers.
    - Use appropriate formatting (e.g., Markdown) to enhance readability.
    - Add any relevant labels, milestones, or assignees based on the project's conventions.

5. Final output:
    - Present the complete GitHub issue content in `<github_issue>` tags.
    - Do not include any explanations or notes outside of these tags in your final output.

Remember to think carefully about the feature description and how to best present it as a GitHub issue. Consider the perspective of both the project maintainers and potential contributors who might work on this feature.

Your final output should consist of only the content within the `<github_issue>` tags, ready to be copied and pasted directly into GitHub. 

After drafting the issue content, create it using `gh issue create`:

**Issue Creation Guidelines:**

1. **Check available labels first**: Run `gh label list` and select the most appropriate label that actually exists. If the label fails to apply, retry without it.

2. **Add to project board if one exists**: After creating the issue, check for user's projects and add the issue to the first/most active one. Set initial status to "Todo" or "Backlog" (whichever exists).

3. **Handle failures gracefully**: If any step fails (label not found, project operations), continue without interrupting the user.

**Remember**: Make intelligent choices based on what's actually available in the repository. Never hardcode values.