#!/bin/bash
# diff.sh COMMIT_A COMMIT_B ...

obelisk_update() {
	if [[ ! -d "obelisk/.git" ]]
	then
		git clone https://github.com/arkutils/Obelisk.git obelisk
	else
		cd obelisk
		git reset --hard HEAD
		git fetch origin master
		cd ..
	fi
}

obelisk_checkout() {
	cd obelisk
	echo "Checking out $1"
	git reset --hard $1
	#git -c "advice.detachedHead=false" checkout $1 > /dev/null
	cd ..
}

prepare() {
	rm -rf sources target
	mkdir sources target
	cp obelisk/data/asb/*.json sources/
	cp -a obelisk/data/wiki/* sources/
}

pike() {
	shift 2
	python pick.py $@
}

rm -rf a b

obelisk_update
obelisk_checkout $1
prepare
pike $@
mv target a
obelisk_checkout $2
prepare
pike $@
mv target b

mkdir target

for b in b/*.svg
do
	fname=`echo $b | sed 's/^[ab]\///'`
	if [[ ! -f "a/$fname" ]]
	then
		mv "$b" target/
		echo "$fname" >> target/ADDED.txt
	fi
done


for a in a/*.svg
do
	fname=`echo $a | sed 's/^[ab]\///'`
	if [[ ! -f "b/$fname" ]]
	then
		echo "$fname" >> target/REMOVED.txt
	else
		sum_a=`cat "$a" | sha256sum`
		sum_b=`cat "b/$fname" | sha256sum`
		if [[ "$sum_a" != "$sum_b" ]]
		then
			mv "b/$fname" target/ 
			echo "$fname" >> target/CHANGED.txt
		fi
	fi
done

diff -u a/species.txt b/species.txt > target/DINODIFF.txt
diff -u a/blacklist.txt b/blacklist.txt > target/BLACKLISTDIFF.txt

