./compile.sh

function req {
  echo $1
  if [ -s "$1" ]
  then
    cat lift.lps | lps2pbes -f $1 | pbes2bool $2
  else
    echo "TODO"
  fi
}


req requirements/deadlock.mcf
req requirements/req1a.mcf
req requirements/req1b.mcf
req requirements/req2.mcf
req requirements/req3.mcf '-gspm'
req requirements/req4.mcf
req requirements/req5a.mcf
req requirements/req5b.mcf
req requirements/req6.mcf
req requirements/req7.mcf
req requirements/req8.mcf
req requirements/req9.mcf
req requirements/req10.mcf
req requirements/req11.mcf
