# Resume Next Steps

## If the goal is to finish the desktop app

1. Repair Japanese strings in [app/i18n.py](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/app/i18n.py:1)
2. Clean up the broken tree section in [README.md](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/README.md:1)
3. Add tests for serializer, validator, schema validator, and filename generation
4. Rebuild the Windows executable

## If the goal is to start the Web app

1. Create a new sibling folder such as `USVmetaGUI-web`
2. Copy or share the reusable logic modules:
   `models.py`, `serializer.py`, `validator.py`, `schema_validator.py`, `repositories.py`
3. Build the first Web flow:
   home -> template select -> record form -> preview -> save
4. Add template/user management after the first save flow works

## Files to read first

- [PROJECT_CONTEXT.md](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/PROJECT_CONTEXT.md:1)
- [README.md](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/README.md:1)
- [app/main_window.py](/C:/Users/rtach/Dropbox/Projects/USVtech/USVmetaGUI/app/main_window.py:1)
