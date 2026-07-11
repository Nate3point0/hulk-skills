# Verified action recipes

Each recipe is a dict for the `WFWorkflowActions` array. Identifiers and
parameter shapes verified against a working import (July 2026). When you
need an action not listed here, build the shortcut manually once in the
Shortcuts app, export/inspect it, and add the recipe — do not guess
identifiers.

## Ask for Text
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.ask</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFAskActionPrompt</key><string>Your prompt here</string>
    <key>WFInputType</key><string>Text</string>  <!-- or Number, URL, Date -->
    <key>UUID</key><string>ASSIGN-A-UUID-HERE</string>
  </dict>
</dict>
```

## Rename file (Set Name)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.setitemname</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFInput</key>
    <dict>
      <key>Value</key><dict><key>Type</key><string>ExtensionInput</string></dict>
      <key>WFSerializationType</key><string>WFTextTokenAttachment</string>
    </dict>
    <key>WFName</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>string</key><string>&#65532;</string>
        <key>attachmentsByRange</key>
        <dict>
          <key>{0, 1}</key>
          <dict>
            <key>Type</key><string>ActionOutput</string>
            <key>OutputUUID</key><string>UUID-OF-ASK-ACTION</string>
            <key>OutputName</key><string>Provided Input</string>
          </dict>
        </dict>
      </dict>
      <key>WFSerializationType</key><string>WFTextTokenString</string>
    </dict>
    <key>WFDontIncludeFileExtension</key><true/>  <!-- keeps .mov/.mp4 -->
  </dict>
</dict>
```

## Save File (user picks destination; iOS remembers Recents)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.documentpicker.save</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFAskWhereToSave</key><true/>
  </dict>
</dict>
```
Hardcoded destination works ONLY for iCloud Drive:
`WFAskWhereToSave: false`, `WFFileDestinationPath: /Shortcuts/subfolder`.

## Get Contents of URL (webhook / API call — the escape hatch)
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.downloadurl</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFURL</key><string>https://your-endpoint.example/hook</string>
    <key>WFHTTPMethod</key><string>POST</string>
    <key>WFHTTPBodyType</key><string>JSON</string>
    <key>WFJSONValues</key>
    <dict>
      <key>Value</key>
      <dict>
        <key>WFDictionaryFieldValueItems</key>
        <array>
          <dict>
            <key>WFItemType</key><integer>0</integer>
            <key>WFKey</key>
            <dict><key>Value</key><dict><key>string</key><string>message</string>
            <key>attachmentsByRange</key><dict/></dict>
            <key>WFSerializationType</key><string>WFTextTokenString</string></dict>
            <key>WFValue</key>
            <dict><key>Value</key><dict><key>string</key><string>hello</string>
            <key>attachmentsByRange</key><dict/></dict>
            <key>WFSerializationType</key><string>WFTextTokenString</string></dict>
          </dict>
        </array>
      </dict>
      <key>WFSerializationType</key><string>WFDictionaryFieldValue</string>
    </dict>
  </dict>
</dict>
```
Rule of thumb: any logic beyond ~5 actions belongs on a server; the
shortcut just POSTs to it (ntfy.sh topics work great as zero-setup
webhooks: POST body to https://ntfy.sh/TOPIC).

## Show Notification
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.notification</string>
  <key>WFWorkflowActionParameters</key>
  <dict>
    <key>WFNotificationActionTitle</key><string>Done</string>
    <key>WFNotificationActionBody</key><string>Saved to Drive</string>
  </dict>
</dict>
```

## Copy to Clipboard
```xml
<dict>
  <key>WFWorkflowActionIdentifier</key>
  <string>is.workflow.actions.setclipboard</string>
  <key>WFWorkflowActionParameters</key><dict/>
</dict>
```

## Other verified identifiers (params discoverable by export-inspect)
- `is.workflow.actions.gettext` — Text block (WFTextActionText)
- `is.workflow.actions.conditional` — If (GroupingIdentifier + WFControlFlowMode 0/1/2)
- `is.workflow.actions.choosefrommenu` — Menu
- `is.workflow.actions.date` — Current date
- `is.workflow.actions.format.date` — Format date
- `is.workflow.actions.openurl` — Open URL
- `is.workflow.actions.savetocameraroll` — Save to Photos
- `is.workflow.actions.encodemedia` — Encode/convert media
- `is.workflow.actions.speaktext` — Speak text
