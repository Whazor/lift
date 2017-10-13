./compile.sh; cat lift.lps | lps2pbes -f $1 | pbes2bool -c | sed '/False$/q'
