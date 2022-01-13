# Assumes that util.py is correct/finished and in current working directory
# Assumes that directory structure is as provided
correctness:
	make decomp FILE=arrow.png
	make decomp FILE=oval.png
	make single FILE=test.1.txt
	make single FILE=arrow.png
	make single FILE=oval.png

## Be careful of effects of image cache
server:
	(cd wwwroot; python3 ../webserver.py)

decomp:
	python3 decompress.py $(FILE).huf.answer
	cmp $(FILE) $(FILE).huf.answer.decomp
	cksum $(FILE) $(FILE).huf.answer.decomp

single:
	python3 compress.py $(FILE)
	python3 decompress.py $(FILE).huf
	cmp $(FILE) $(FILE).huf.decomp
	cksum $(FILE) $(FILE).huf.decomp

clean:
	-rm arrow.png.huf
	-rm arrow.png.huf.decomp
	-rm oval.png.huf
	-rm oval.png.huf.decomp
	-rm test.1.txt.huf
	-rm test.1.txt.huf.decomp
	-rm arrow.png.huf.answer.decomp
	-rm oval.png.huf.answer.decomp
	-rm -r -f __pycache__
