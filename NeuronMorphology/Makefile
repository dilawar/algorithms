all :
	./swc_tool.py -i ./cells/4H-2traced-1.CNG.swc -p -im 

test: 
	find . -type f -name "*.swc" | xargs -I file ./swc_tool.py -i file -p -im 
