# Admin_Beacon
A script to find admin login pages and directories (GET) with user-defined directory prefixes enabled
#### Features
- [x] Multi-threading on demand
- [x] path list 
- [x] Supports php, asp and html extensions
- [x] Checks for potential EAR vulnerabilites
- [x] Checks for robots.txt
- [x] Support for custom patns

### Usages
- Check all paths with php extension
```
python admin-beacon -u example.com --type php
```
- Check all paths with php extension with threads
```
python admin-beacon -u example.com --type php --fast
```
- Check all paths without threads
```
python admin-beacon -u example.com
```
- Adding a custom path. For example if you want all paths to start with /data (example.com/data/...) you can do this:
```
python admin-beacon -u example.com --path /data
```

