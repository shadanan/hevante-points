Hevante.zip: src/lambda_function.py
	rm -f build/Hevante.zip
	mkdir -p build
	cd src; zip -rXq ../build/Hevante.zip .
