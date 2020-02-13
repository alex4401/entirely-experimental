for f in `ls *.src.*`
do
	o="`echo $f | sed 's/\.src//'`"
	openssl enc -aes-256-cbc -in $f -base64 -pbkdf2 > $o
done
