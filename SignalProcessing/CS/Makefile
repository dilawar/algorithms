IMAGES= ./figure_compressend_sensing.pdf ./figure_solution.pdf \
	./figure_compressend_sensing_DCT.pdf ./figure_measurements.pdf

all : ./compressed_sensing.png ./magic_reconstruction.png  compressed_sensing.pdf compressed_sensing.html 
	@echo "All done"

compressed_sensing.pdf : compressed_sensing.pandoc $(IMAGES)
	~/Scripts/pandoc2pdf.sh $<

compressed_sensing.html : compressed_sensing.pandoc $(IMAGES)
	~/Scripts/pandoc2wordpress.py $<

%.png : %.py 
	PYTHONPATH=~/Work/GITHUB/DILAWAR/pypgfplots/ python $<

%.pdf : %.tex
	lualatex --shell-escape $<
