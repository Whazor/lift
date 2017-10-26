Z=$1
shift
./compile.sh; cat lift.lps | lps2pbes -f $Z | pbes2bool $@ | sed '/False$/q'
