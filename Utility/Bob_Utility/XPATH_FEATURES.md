# XPath Finder Features

## Two Separate Features Available

### 1. Execute XPath Query (Traditional)
**Button:** 🔍 Execute XPath
**Purpose:** Run a custom XPath expression on your XML
**Input:** 
- XML content
- XPath expression (e.g., `//book/title`)
**Output:** 
- List of matching elements
- Element details (tag, text, attributes)

**Example:**
```
Input XPath: //book/title
Output: Shows all book titles found
```

---

### 2. Find XPath by Value (New Feature)
**Button:** 🎯 Find XPath by Value
**Purpose:** Search for a value and get its XPath automatically
**Input:**
- XML content
- Value to search for (e.g., "1977-05-07")
**Output:** 
- **Standard XPath** with positions: `/Envelope[1]/Body[1]/Change_Personal_Information_Response[1]/Personal_Information_Data[1]/Date_of_Birth[1]`
- **Local-name XPath** (namespace-agnostic): `//*[local-name()='Date_of_Birth']/text()`
- Element tag and value

**Example Output:**
```
Found 1 match(es) for value: "1977-05-07"

Match 1:
  Standard XPath: /Envelope[1]/Body[1]/Change_Personal_Information_Response[1]/Personal_Information_Data[1]/Date_of_Birth[1]
  Local-name XPath: //*[local-name()='Date_of_Birth']/text()
  Element: <Date_of_Birth>
  Value: 1977-05-07
```

---

## Why Two XPath Formats?

### Standard XPath
- Uses full path with positions
- Precise and unambiguous
- Works with or without namespaces
- Example: `/Envelope[1]/Body[1]/Date_of_Birth[1]`

### Local-name XPath
- Namespace-agnostic (works regardless of namespace prefixes)
- Shorter and more readable
- Perfect for SOAP/XML with namespaces
- Example: `//*[local-name()='Date_of_Birth']/text()`

---

## How to Use

### Execute XPath:
1. Paste XML in the text area
2. Enter your XPath expression in "XPath Expression" field
3. Click "🔍 Execute XPath"
4. View matching elements

### Find XPath by Value:
1. Paste XML in the text area
2. Enter the value you're looking for in "Find XPath by Value" field
3. Click "🎯 Find XPath by Value"
4. Get both XPath formats automatically
5. Use the copy button to copy results

---

## Test Files Available
- `test_xpath_finder.xml` - Simple library example
- `test_workday_soap.xml` - Workday SOAP example with namespaces