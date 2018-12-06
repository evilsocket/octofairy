all: train

train: convert
	@ergo train . --dataset "tools/data.csv"

convert:
	@./tools/convert-repo-info.py --folder "$(GITHUB_REPO)" --to "tools/data.csv"
	
download:
	@./tools/download-repo-info.py --repo "$(GITHUB_REPO)" --api-token "$(GITHUB_API_KEY)"

requirements:
	@sudo pip3 install -r tools/requirements.txt

clean:
	@ergo clean . --all > /dev/null 2>&1
	@rm -rf tools/data.csv
