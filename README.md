# Crispy Octo Succotash

**Problem Statement: Refactor the Blogs Update Controller to Follow Hexagonal Architecture and DDD Best Practices.**

## Context

A blog platform exposes an endpoint for updating blog posts. The current implementation has a single controller method (`BlogsA0Controller.update_blog`) that receives a DTO with optional `title` and `body` fields, along with user authentication and audit metadata (user agent, IP address).

## Current State

The codebase has the right structural bones (domain, infrastructure, application layers) but the layers are not properly separated:

- **Entities are not immutable** — mutable entities risk accidental state corruption.
- **The repository leaks raw dicts** — `fetch_blog` and `save` should exchange domain entities, not dictionaries.
- **The service mutates entities in place** — instead of producing new immutable instances.
- **The controller does not wire dependencies** — it accepts no constructor arguments and cannot be tested in isolation.
- **Audit logging is incomplete** — the `_log_audit_event` method exists but is never called during updates.
- **Naming is inconsistent** — `BlogService` vs `BlogsService`, `UsersRepository` vs `UserRepository`, camelCase keys in dicts vs snake_case in entities.

## Goal

Evolve the code so that:

1. **Entities are immutable** — frozen dataclasses with `from_dict()` / `to_dict()` for hydration and serialization, and `dataclasses.replace()` for producing updated versions.

2. **The repository is the mapping layer** — it turns raw dicts into domain entities on read, and domain entities back into dicts on write. It never exposes raw data to the service layer.

3. **The service owns the business logic** — it validates the user exists, the blog exists, collects changed fields, produces a new entity via `replace()`, and persists it through the repository.

4. **The controller owns the orchestration** — it wires the dependency chain, maps HTTP concerns (DTOs, user agent, IP) to service calls, and manages audit logging.

5. **Audit logging is wired into the update flow** — before persisting, the controller logs what changed (old value, new value, who did it, when).

6. **Naming is consistent** — singular for entities and repositories (`Blog`, `UserRepository`), plural for collections and services (`BlogsService`).

## Success Criteria

The `update_blog` endpoint works end-to-end, returns the updated blog, audit logs are populated, and no layer knows about the internals of another layer. The code is testable by injecting mock repositories.

## Architecture

```
python/
  main.py                              # entry point
  blogs/
    application/
      blogs_controller.py              # orchestrates service + audit
    domain/
      entities/
        blog_entity.py                 # immutable Blog
      services/
        blogs_service.py               # business logic (validate, replace, save)
    infrastructure/
      blogs_repository.py              # mapping layer (dict <-> entity)
  users/
    domain/
      entities/
        user_entity.py                 # immutable User
    infrastructure/
      user_repository.py               # mapping layer (dict <-> entity)
```

## Flow

```
Controller.update_blog()
  -> BlogsService.update_blog()          # validate user, validate blog, collect changes
  -> dataclasses.replace(blog, **changes) # produce new immutable entity
  -> BlogsRepository.save(updated_blog)  # persist (entity -> dict)
  -> Controller._log_audit_event()       # record what changed
  -> return { success, blog, audit_id }  # response
```

## Progress

- [x] Fixed `python.` prefix in imports (module resolution)
- [x] Added `__init__.py` files for package resolution
- [x] Made `User` entity immutable (`frozen=True`) with `from_dict()`
- [x] Made `Blog` entity immutable (`frozen=True`) with `from_dict()` / `to_dict()`
- [x] `UserRepository.fetch_user()` returns `User | None` (not raw dict)
- [x] `BlogsRepository.fetch_blog()` returns `Blog | None` (not raw dict)
- [x] `BlogsRepository.save()` accepts a `Blog` entity, persists via `to_dict()`
- [x] `BlogsService.update_blog()` uses `dataclasses.replace()` instead of in-place mutation
- [x] `BlogsA0Controller` wires dependencies in constructor
- [ ] Wire audit logging into the update flow
- [ ] Add unit tests with mock repositories
- [ ] Add integration test
