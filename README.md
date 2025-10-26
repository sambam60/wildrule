# Team10project



```
cd existing_repo
git remote add origin https://git.cardiff.ac.uk/c25094498/team10project.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://git.cardiff.ac.uk/c25094498/team10project/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)


## Name
We need to make a name

## Description

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Requirements (offline TTS/ASR):

1. Python packages (install in your environment):
```
pip install pyttsx3 vosk sounddevice numpy
```

2. Vosk offline model (no internet needed at runtime):
   - Download `vosk-model-small-en-us-0.15` from `https://alphacephei.com/vosk/models`
   - Extract to `assets/models/vosk/vosk-model-small-en-us-0.15`
   - Create folders if they don't exist.

Notes:
- On macOS, you may need to grant microphone permissions or install PortAudio (`brew install portaudio`).
- If TTS fails to initialise, the game will continue without speaking.

## Usage
Run the game:
```
python game.py
```

At startup you will be asked:
- "Enable Text-To-Speech (y/n)?"
- "Enable Voice Input (y/n)?"

If voice input is enabled, when prompted for a command the terminal shows a live ASCII sparkline of microphone peaks while listening. Speak your command; recognition stops on silence or timeout and the text is echoed. If recognition fails or times out, the game falls back to keyboard input.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
MIT License

## Project status
In development until Tuesday the 28th of October

## Troubleshooting
- No speech output: ensure `pyttsx3` installed and system audio output works. Some environments require `espeak`/`nsss` backends.
- Mic not working: install PortAudio and allow microphone permissions. Verify with `python -c "import sounddevice as sd; print(sd.query_devices())"`.
- Model not found: check the Vosk model path `assets/models/vosk/vosk-model-small-en-us-0.15` exists.