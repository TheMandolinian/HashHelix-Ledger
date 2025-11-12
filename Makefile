.PHONY: seal verify latest sv selftest
seal:
	python3 scripts/epoch_tools.py seal
verify:
	python3 scripts/epoch_tools.py verify "epochs/epoch-*.json"
latest:
	python3 scripts/epoch_tools.py verify "$(ls -1 epochs/epoch-*.json | tail -n1)"
sv: seal verify
selftest:
	bash scripts/selftest.sh
