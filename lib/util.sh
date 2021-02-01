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
  while ! docker-compose exec postgresql pg_isready -h localhost -U postgres -d ohdsi -q; do
    sleep 10
    printf "."
  done
  echo
}

psql_table_exists() {
  schema="$1"
  table="$2"
  source_exists_query="SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = '${schema}' AND tablename = '${table}');"
  docker-compose exec postgresql psql -h localhost -U postgres -c "${source_exists_query}" -tq ohdsi | grep -qe "^[[:space:]]*t[[:space:]]*$"
  return $?
}

psql_wait_table() {
  while ! psql_table_exists "$1" "$2"; do
    sleep 10
    printf "."
  done
  echo
}
