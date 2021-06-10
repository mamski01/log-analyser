# Error log analyser

This small application is meant to analyse the main errors log (*at least for now*)

### How it works?

1. Create a dictionary by feeding log files
2. Give a definition for the entries in the dictionary
3. Use the dictionary to analyse new logs

---
## Under the hood

### How do we create our dictonary?

1. Run through each line of the log
2. Remove timestamps
3. Remove clutter
4. Register the remaining message in the dictionary (`hash table`)
5. Go through the new dictionary entries and give them a definition/description

### How do we make the log readable?

1. Run through the same process as for the dictionary to clean the data
2. Compare it to the dictionary hash table
3. Replace the entries with the definition inside the dictionary

### Dictionary model

```json
{
    "message hash":[
        "original message",
        "interpreted message",
        "error group"
    ]
}
```
### Middle model

```json
{
    "message hash":[
        "timestamp",
        "
    ]
}
```

### Notes for self

1. Change the dictionary to include verbose keys for better reading