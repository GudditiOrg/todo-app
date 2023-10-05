# Create Task

```Yaml
curl --location 'http://localhost/tasks/' \
--header 'Content-Type: text/plain' \
--data '{
    "title": "next task "
}
'
```

# List Tasks

```Yaml
curl --location 'http://localhost/tasks'

```

# delete tasks

```Yaml
curl --location --request DELETE 'http://localhost/tasks/651e44275a2ca252bedfe5a2'

```

> Replace localhost with your ip or endpoint
