inFile=$1

nCG=`grep -o "CG" $inFile | wc -l`
nTG=`grep -o "TG" $inFile | wc -l`
ratio=`echo "scale=3;$nCG/$nTG" | bc`
avgMeth=`echo "scale=3;$nCG/($nCG+$nTG)"| bc`
echo -e "$inFile\tnCG=$nCG\tnTG=$nTG\tavgMeth=$avgMeth"
