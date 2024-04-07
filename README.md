# APM API

## Run
```sh
uvicorn main:app --reload
```

## URLs list:
 - /
 - /get/plazas
 - /get/plazas/{user_id}
 - /put/new_user/{user_id}/{user_name}
 - /put/user/{user_id}/add_favorite/{slot_id}
 - /put/user/{user_id}/remove_favorite/{slot_id}
 - /put/user/{user_id}/edit_info/{new_name}