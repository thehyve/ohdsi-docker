# Load files and replace all environment variables $ENV as
# their values. To disable this for a given variable, escape it as
# \$ENV.
cat-env() {
  E="$(cat "$@")"
  while IFS='=' read -r name value ; do
    value="$(sed -e 's/[\/&]/\\&/g' <<< "$value")"
    E="$(sed -e "s/\${$name}/$value/g" <<< "$E")"
  done < <(env)
  echo "$E"
}

psql_wait_ready() {
  counter=1
  until docker-compose --log-level CRITICAL exec postgresql pg_isready -h localhost -U postgres -d ohdsi -q; do
    sleep 1
    printf "."
    if [ $counter -eq 10 ]
    then
        echo
        docker-compose --log-level DEBUG exec postgresql pg_isready -h localhost -U postgres -d ohdsi
        break
    fi
    counter=$(( $counter + 1 ))
  done
  echo
}

psql_table_exists() {
  schema="$1"
  table="$2"
  local level="${3:-CRITICAL}"
  source_exists_query="SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = '${schema}' AND tablename = '${table}');"
  docker-compose --log-level "${level}" exec postgresql psql -h localhost -U postgres -c "${source_exists_query}" -tq ohdsi | grep -qe "^[[:space:]]*t[[:space:]]*$"
  return $?
}

psql_wait_table() {
  counter=1
  until psql_table_exists "$1" "$2"; do
    sleep 1
    printf "."
    if [ $counter -eq 10 ]
    then
        echo
        psql_table_exists "$1" "$2" "DEBUG"
        break
    fi
    counter=$(( $counter + 1 ))
  done
  echo
}
