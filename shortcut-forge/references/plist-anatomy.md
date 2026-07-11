# .shortcut plist anatomy (verified working — July 2026)

A `.shortcut` file is a plist. This exact skeleton built and imported
successfully ("Send Clip to Hulk"). Replace the actions array per recipe.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>WFWorkflowClientVersion</key>
    <string>2605.0.5</string>
    <key>WFWorkflowMinimumClientVersion</key>
    <integer>900</integer>
    <key>WFWorkflowMinimumClientVersionString</key>
    <string>900</string>
    <key>WFWorkflowHasOutputFallback</key>
    <false/>
    <key>WFWorkflowHasShortcutInputVariables</key>
    <true/>  <!-- true if any action references ExtensionInput -->
    <key>WFWorkflowIcon</key>
    <dict>
        <key>WFWorkflowIconStartColor</key>
        <integer>4274264319</integer>   <!-- blue; 4292093695 red, 4271458815 green -->
        <key>WFWorkflowIconGlyphNumber</key>
        <integer>59511</integer>
    </dict>
    <key>WFWorkflowImportQuestions</key>
    <array/>
    <key>WFWorkflowTypes</key>
    <array>
        <string>ActionExtension</string>  <!-- share sheet; omit array contents for plain shortcuts -->
    </array>
    <key>WFWorkflowInputContentItemClasses</key>
    <array>
        <string>WFAVAssetContentItem</string>     <!-- video/audio -->
        <string>WFGenericFileContentItem</string>
        <!-- others: WFImageContentItem, WFURLContentItem, WFStringContentItem,
             WFPDFContentItem, WFRichTextContentItem, WFSafariWebPageContentItem -->
    </array>
    <key>WFWorkflowActions</key>
    <array>
        <!-- action dicts here, executed top to bottom;
             each action's output flows to the next unless WFInput overrides -->
    </array>
</dict>
</plist>
```

## Magic variable wiring

Give any action whose output you need a `UUID` param, then reference it:

```xml
<!-- inside a WFTextTokenString value -->
<key>string</key><string>&#65532;</string>
<key>attachmentsByRange</key>
<dict>
  <key>{0, 1}</key>
  <dict>
    <key>Type</key><string>ActionOutput</string>
    <key>OutputUUID</key><string>THE-UUID-YOU-ASSIGNED</string>
    <key>OutputName</key><string>Provided Input</string>
  </dict>
</dict>
```

Share-sheet input reference (as a WFTextTokenAttachment for WFInput):

```xml
<dict>
  <key>Value</key>
  <dict><key>Type</key><string>ExtensionInput</string></dict>
  <key>WFSerializationType</key><string>WFTextTokenAttachment</string>
</dict>
```

Other attachment Types: `CurrentDate`, `Clipboard`, `Ask` (ask each time),
`Variable` (named variable, add `VariableName`).
