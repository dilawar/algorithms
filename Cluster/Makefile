all : solve #./network.png ./flow.png


%.png : %.dot 
	dot -Tpng $< -o $@

./network.dot ./flow.dot : ./cluster.py
	python $<

solve : ./cluster.py
	python $<
