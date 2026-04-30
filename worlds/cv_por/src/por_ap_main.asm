.nds
.relativeinclude on
.erroronwarning on

@Overlay119Start equ 0x02308EC0
@FreeSpace equ @Overlay119Start + 0x60

@ServerItemType equ 0x02308ED0 ; 2 bytes
@TotalItemsReceived equ 0x02308ED2 ; 2 bytes

@OptionFlag_BraunerRequired equ 0x1
@OptionFlag_NestRequired equ 0x2

;;;;;;;;;;;;;;;;;
.open "ftc/arm9.bin", 02000000h
    .org 0x020523B0
        bl @GetRemoteItem

    .org 0x02041DB4
        bl @SaveAPData

    .org 0x0203A30C
        nop ; Infinite-use Magical Tickets

    .org 0x0203A24C
        ands r0, r0, 0x80000007 ; Allow tickets before having saved the game

    .org 0x0203A26C
        b 0203A27Ch ; Allow ticket use before visiting the shop

    .org 0x0204FEC4
        bl @AddCyanPaletteToItemNames

    .org 0x0204FE94
        bl @UseOverrideColor

    .org 0x02042388
        bl @LoadAPData ; The game loads file X when copying data. Load in the relevant AP data so it gets copied as well.

    .org 0x020423A4
        bl @SaveAPData ; The game saves file Y when copying data. Save the AP data we JUST copied out of the old file into the new one.

    .org 0x02079294
        bl @CheckPresenceOfLocket

    .org 0x0203B65C
        b @DontEquipOnGlitchMenu

    .org 0x02079874
        bl @PostBraunerCheck

    .org 0x02076B84
        b @CheckBraunerRequirements

    .org 0x0206EAA0
        bl @ShowBreakableWalls

    .org 0x02040554
        b @BetterQuestHandler

    .org 0x02040AE0
        b @GetQuestRewardText

    .org 0x02040C94
        bl @GetQuestRewardDesc

    .org 0x020E537C
        .dw  @PostBehemothRoom

    ; Fix the map explore/suspend bug
    .org 0x0202E5F8
        push r4-r10,r14
        
        ldr r4, =020FCAB0h
        ldr r5, =020FCC10h
        ldr r6, =02111778h
        ldrh r7, [r6] ; Read room's x pos from 02111778
        ldrh r8, [r6, 2h] ; Read room's y pos from 0211177A
        
        ldr r0, [r4] ; Read player 1's x pos from 020FCAB0
        bl @ClampXPosToRoomWidth
        add r0, r0, r7 ; Add player 1's x to room's x
        strh r0, [r6, 4h] ; Store player 1's x on map to 0211177C
        
        ldr r0, [r5] ; Read player 2's x pos from 020FCC10
        bl @ClampXPosToRoomWidth
        add r0, r0, r7 ; Add player 2's x to room's x
        strh r0, [r6, 6h] ; Store player 2's x on map to 0211177E
        
        ldr r0, [r4, 4h] ; Read player 1's y pos from 020FCAB4
        bl @ClampYPosToRoomHeight
        add r0, r0, r8 ; Add player 1's y to room's y
        strh r0, [r6, 8h] ; Store player 1's y on map to 02111780
        
        ldr r0, [r5, 4h] ; Read player 2's y pos from 020FCC14
        bl @ClampYPosToRoomHeight
        add r0, r0, r8 ; Add player 2's y to room's y
        strh r0, [r6, 0Ah] ; Store player 2's y on map to 02111782
        
        
        ; The rewritten first half of the function now correctly updates the players' positions on the map.
        ; But the second half of the function which updates the tile being explored needs certain values to be in certain registers to work correctly.
        ; So we initialize those registers here.
        ldrb r4, [r6, 0Dh] ; r4 has current area index read from 02111785
        mov r0, r4
        bl 02030570h ; MapGetExploredTileListForArea
        mov r5, r0 ; r5 has current area's explored tile list pointer
        mov r0, r4 ; ; r0 has current area index
        ldr r7, =020CA580h ; PointerToGameObject
        ldr r14, =1B50Ch
        ldr r6, =1B510h
        b 0202E6CCh
        .pool

.close
;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_0", 021CDF60h
    ; If we own 9 of an item, pretend we have 8
    ; this allows the item to still be properly picked up even at cap
    .org 0x021E4400 ; In GiveItem
        movge r9, 8
        nop
        nop

    .org 0x021E5A30
        nop ; Prevent the game from not letting you pick up 9 of a skill. This is autocapped anyways...

    .org 0x021E4418
        bl @SpecialItemHandler

    .org 0x021FCA80
        bl @InitializeNewGameData

    .org 0x021E5414
        bl @LoadAPItemColor

;;;;;;;;;;;;;;;;
    .org 0x0221BBBC  ; Repoint the Konami Man and Twin Bee's item names
        .dw 0x0222253C ; This so that they can both use the name 'AP Item'
        .dw 0x0222253C
;;;;;;;;;;;;;;;;;;;;;
;overlay 9 0
.close

.open "ftc/overlay9_1", 0x0221F680
    .org 0x0222253E
        .db 0x21, 0x30, 0x00, 0x49, 0x54, 0x45, 0x4D, 0xEA ; AP Item - editor repoints text so im doing it here manually
.close
;;;;;;;;;;;;;;;;;;;;;;

.open "ftc/overlay9_2", 0x0221F680
    .org 0x0222B076
        ; The Management says we shouldn't enter this portrait
        ; without Stella's locket...
        .db 0x34, 0x48, 0x45, 0x00, 0x2D, 0x41, 0x4E, 0x41, 0x47, 0x45, 0x4D, 0x45, 0x4E, 0x54, 0x00, 0x53
        .db 0x41, 0x59, 0x53, 0x00, 0x57, 0x45, 0x00, 0x53, 0x48, 0x4F, 0x55, 0x4C, 0x44, 0x4E, 0x07, 0x54
        .db 0x00, 0x45, 0x4E, 0x54, 0x45, 0x52, 0xE6, 0x54, 0x48, 0x49, 0x53, 0x00, 0x50, 0x4F, 0x52, 0x54
        .db 0x52, 0x41, 0x49, 0x54, 0x00, 0x57, 0x49, 0x54, 0x48, 0x4F, 0x55, 0x54, 0x00, 0x33, 0x54, 0x45
        .db 0x4C, 0x4C, 0x41, 0x07, 0x53, 0x00, 0x4C, 0x4F, 0x43, 0x4B, 0x45, 0x54, 0x0E, 0x0E, 0x0E, 0xE5
        .db 0xE4

        ;...?
        ;...Who the hell is "The Management?!"
        .db 0xE7, 0x00, 0xE3, 0x09, 0x0E, 0x0E, 0x0E, 0x1F, 0xE5, 0xE9, 0xE3, 0x02, 0x0E, 0x0E, 0x0E, 0x37
        .db 0x48, 0x4F, 0x00, 0x54, 0x48, 0x45, 0x00, 0x48, 0x45, 0x4C, 0x4C, 0x00, 0x49, 0x53, 0x00, 0x02
        .db 0x34, 0x48, 0x45, 0x00, 0x2D, 0x41, 0x4E, 0x41, 0x47, 0x45, 0x4D, 0x45, 0x4E, 0x54, 0x02, 0x1F
        .db 0x01, 0xE5, 0xE4

        ; Me.
        ; I'm The Management.
        .db 0xE7, 0x01, 0xE3, 0x0B, 0x2D, 0x45, 0x0E, 0xE6, 0x29, 0x07, 0x4D, 0x00, 0x54, 0x48, 0x45, 0x00
        .db 0x4D, 0x41, 0x4E, 0x41, 0x47, 0x45, 0x4D, 0x45, 0x4E, 0x54, 0x0E, 0xE5, 0xE4

        ; Well, I guess I can't really
        ; argue with that...
        .db 0xE7, 0x00, 0xE3, 0x05, 0x37, 0x45, 0x4C, 0x4C, 0x0C, 0x00, 0x29, 0x00, 0x47, 0x55, 0x45, 0x53
        .db 0x53, 0x00, 0x29, 0x00, 0x43, 0x41, 0x4E, 0x07, 0x54, 0x00, 0x52, 0x45, 0x41, 0x4C, 0x4C, 0x59
        .db 0xE6, 0x41, 0x52, 0x47, 0x55, 0x45, 0x00, 0x57, 0x49, 0x54, 0x48, 0x00, 0x54, 0x48, 0x41, 0x54
        .db 0x0E, 0x0E, 0x0E, 0xE6, 0xE5, 0xE4, 0xEA
.close
;;;;;;;;;;;;
.open "ftc/overlay9_4", 0x0222C840
    .org 0x02232864
        nop ; Prevent the game from deleting the old vampire killer

    .org 0x02232890
        nop ; Prevent the game from giving you the new Vampire Killer, we do this in the next room instead

    .org 0x02232880
        nop ; Prevent the game from auto-equipping new Vampire Killer.
.close
;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_25",  0x022D7900
    .org 0x022D95CC
        bl @LoadAPData

.close


;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_27", 0x022E01A0
    .org 0x022E04B8 ; Skip to the title screen instantly instead of 6 years of fucking logos
        mov r0, 0x77
        bl 0x02007970 ; Load our custom overlay so the original code doesnt get screwed with?
.close
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_60", 0x022D7900
    ; Fix the enemy version of the creature setting the boss kill flag
    .org 0x022D7D14
    ldrh r1, [r1, 3Ch]
    cmp r1, 0h
    beq 0x022D7D30
    
    ; Then set the boss death flag.
    ldr r2, [r0, 76Ch]
    orr r2, r2, 200h
    str r2, [r0, 76Ch]
.close

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_64", 022D7900h
    .org 0x022D8B18  ; Prevents death's cutscene skip from setting his flag too early
        nop

    .org 0x022E4F94
        nop ; Prevent dracula from setting the dracula flag mid fight
.close
;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_78", 0x022E8820
    .org 0x022E8884
        cmp r1, 0xFF ; Always set the drawbridge to open

    .org 0x022E898C
        bl @Undergroundpassage_Portraitcheck
.close

.open "ftc/overlay9_79", 0x022E8820
    .org 0x022E9348
        b 0x022E9364 ; Skips Wind's locket cutscene, removed for brevity
.close
;;;;;;;;
;Tile data for the tower room. adds platforms
.open "ftc/overlay9_85", 0x022E8820
    .org 0x022F3FA4
        .dh 0x0044
        .dh 0x0045
        .dh 0x0044
        .dh 0x0047
.close
;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_86", 0x022E8820
    .org 0x022EC2BC
        nop ; Skip over giving the original locket

    .org 0x022EC304
        bl @GiveLocketItem

    .org 0x022EC8EC
        b 0x022EC900 ; Forest of Doom portrait. Ignore the shortened dialogue so I can write my own thing here

    .org 0x022EC8A0
        b @ForestPortraitSceneCheck
.close
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_88", 0x022E8820
    .org 0x022E8880
        b @CheckDraculaBarrierRequirements
.close

.open "ftc/overlay9_89", 0x022E8820
    .org 0x022EA018
        bl @GetWhipMemItem
.close
;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_90", 0x022E8820
    .org 0x022E8BD8
        bl @EndDracula
.close
;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_111", 0x022E8820
; Breakable ceiling that lets rain through from Dark Academy.
.org 0x022E8FEC
  bl @ShowBreakableWalls
.close
;;;;;;;;;;;;;;;;;;;;;;;

.open "ftc/overlay9_119", @Overlay119Start

.org @FreeSpace
.area 0x1F000 ; Maximum overlay space, failsafe if too big
;;;;;;;;;;;;;;;;;
;2308F20
@AP_playerauth: ; Used for the Player name as well as the current world version
    .fill 0x20

;2308F40
@ItemColorTable:
    .fill 0x200 ; This space is reserved for AP item tag colors
.align 4

;2309140
@PostBehemothRoom:
    .dh 0x00E8 ; Upper pickup
    .dh 0x0068
    .db 0x00
    .db 0x04
    .db 0x0B
    .db 0x00
    .dh 0x000F
    .dh 0x0069

    .dh 0x00E0 ; Lower pickup
    .dh 0x0140
    .db 0x00
    .db 0x04
    .db 0x08
    .db 0x00
    .dh 0x0040
    .dh 0x0000

    .dh 0x0010 ; Behemoth wall
    .dh 0x0130
    .db 0x00
    .db 0x02
    .db 0x3A
    .db 0x00
    .dh 0x000C
    .dh 0x0000
    .db 0xFF, 0x7F, 0xFF, 0x7F

;02309168
@WhipMemoryItem:
    .dh 0x030A ;02308F28
    .db 0x00 ;02308F2A

;0230916B
@StellaLocketItem:
    .dh 0x0703 ; Type/ID for the locket 02308F25
    .db 0x00 ; Item color 02308F27

;0230916E
@GenerationFlags:
    @OptionFlag_NestPortraits: ;0230916E
        .db 0x08

    @OptionFlag_BraunerPortraits: ;0230916F
        .db 0x04

    @OptionFlag_DraculaPortraits: ;02309170
        .db 0x00

    @OptionFlag_DraculaRequirements: ;02309171
        .db 0x01

    @OptionFlag_DraculaGoal: ;02309172
        .db 0x01

    @OptionFlag_StartWithChangeCube: ;02309173
        .db 0x00

    @OptionFlag_RevealHiddenWalls: ;02309174
        .db 0x00

    @OptionFlag_RevealMap: ;02309175
        .db 0x00

    @OptionFlag_EXPMult: ;02309176
        .db 0x00

    .align 4
;;;;;;;;;;;;;;;;;;;
; Gets an arbitrary item and gives it to the player. Used for Archipelago server items
;0x02308ED0 - item type
;0x02308ED1 - item ID
@GetRemoteItem:
    push r0-r3, lr

    ldr r0, =0x020F628C ; Does the player have control?
    ldrb r0, [r0]
    cmp r0, 0
    bne @@End ; We don't want to get items while playing text and stuff

    ldr r0, = 0x020FC498
    ldrb r0, [r0]
    cmp r0, 0
    bne @@End ; This is for main player control. Also used for cutscenes/autowalks?

    ldr r0, = 0x0211174C
    ldr r0, [r0]
    ldr r1, = 0x80100041 ; We don't want to get items while dying, in a cutscene, room transition, or otherwise in a no pausing state
    ands r0, r0, r1
    bne @@End

    ldr r0, = @ServerItemType
    mov r1, r0 ; back up the address
    
    ldrh r0, [r0] ; Load the item we've received
    ands r1, r0, 0xFF ; Move the ID to r1
    ands r0, r0, 0xFF00 ; separate the TYPE from the ID
    beq @@End ; If this is 0, assume we haven't received anything

    lsr r0, r0, 0x8
    bl @GetItemArbitrary
    ldr r0, = @ServerItemType
    mov r1, 0
    strh r1, [r0] ; Zero out the item so we don't get anything again
@@End:
    pop r0-r3,lr
    b 0x0201E9C0 ; Return to normal code
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;Gives something to the player.
; r0 = Item TYPE
; r1 = Item ID

@MoneyValues:
.dh 0x0001, 0x000A, 0x0032, 0x0064, 0x01F4, 0x03E8, 0x07D0
.align 4

@RamFlag_SkipArbitrarayPopup:
.db 0x00
.align 4

@GetItemArbitrary:
    push lr
    cmp r0, 1 ; Money
    beq @@GetMoney
    cmp r0, 8
    beq @@GetSkill ; Skills/abilities
    ; normal items/armor
    push r0,r1
    cmp r1, 0x08
    blt @@NormalItem
    cmp r1, 0x0A
    bge @@NormalItem
    b @@GetMaxUp ; ID 8-A are used for max up boosts
@@NormalItem:
    bl 0x021E43E4 ; Subroutine for granting regular items
    pop r0,r1
    bl 0x021E476C ; Get the global ID for the item
    ldr r1, =@RamFlag_SkipArbitrarayPopup
    ldrb r1,[r1]
    cmp r1, 1
    beq @@SkipItemPopup ; If we're in the quest menu we don't want to show popups
    mov r1, 0xF0
    bl 0x0204FE0C ; Display the got item popup
    mov r0, 0x31
    bl 0x0204D6B0 ; Play the sound effect for the item
    @@SkipItemPopup:
    pop lr
    bx lr
@@GetMaxUp:
    pop r0,r1
    mov r0, r1 ; Put the ID in r0
    mov r1, 1
    mov r2, 0
    bl 0x021E3AA8 ; Useconsumable/Get Max Up
    pop lr
    bx lr
@@GetSkill:
    mov r0, r1
    push r0, r1

    ldr r1, =@RamFlag_SkipArbitrarayPopup
    ldrb r1, [r1]
    cmp r1, 1
    beq @@SkipSkillPopup
    
    mov r1, 0xF0
    bl 0x0204FB24 ; Show skill popup

    mov r0, 0x30
    bl 0x0204D6B0 ; Play the sound effect for the item
    @@SkipSkillPopup:
    pop r0, r1
    push r0
    mov r1, 1
    bl 0x02214F34 ; Give the skill
    pop r0

    cmp r0, 0x5C ; Is this a Relic?
    blt @@EndSkill
    sub r0, r0, 0x5C ; get the skill id num
    mov r1, 1
    bl 0x02215308 ; Activate relic
@@EndSkill:
    pop lr
    bx lr
@@GetMoney:
    mov r1, r1, lsl 1
    ldr r0, = @MoneyValues
    ldrh r0, [r0, r1] ; Load the 2 bytes corresponding to the amount
    push r0
    cmp r0, 1000
    bge @@BigMoneySound ; values over $1,000 play special sfx
    mov r0, 0x2B
    b @@SmallMoneySound
@@BigMoneySound:
    mov r0, 0x2C
@@SmallMoneySound:
    bl 0x0204D6B0
    pop r0
    push r0
    bl 0x021E3F24 ; Give this amount of money
    pop r0
    push r2
    ldr r2, =@RamFlag_SkipArbitrarayPopup
    ldrb r2,[r2]
    cmp r2, 1
    beq @@SkipMoneyPopup
    bl 0x0204FD4C ; Show the text popup for it
    @@SkipMoneyPopup:
    pop r2
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;
; Commits some extra data used by AP into SRAM
@SaveAPData:
    push r0-r3
    push lr
    mov r2, 0x50
    mul r0, r0, r2 ; filenum * 0x50

    ldr r1, =0x1F00
    add r0, r0, r1
    ldr r1, =@ServerItemType
    ldr r3, =0x00
    bl 0x020118F4
    pop lr
    pop r0-r3
    b 0x02042C44

; Loads data out of the save file into main ram
@LoadAPData:
    push r0-r3
    push lr
    mov r2, 0x50
    mul r0, r0, r2 ; (Offset is FileNum * 0x50)
    ldr r1, =0x1F00
    add r0, r0, r1 ; Add base offset + file offset
    ldr r1, = @ServerItemType
    bl 0x02011998 ;LoadData
    pop lr
    pop r0-r3
    b 0x02042FA4 ; load the rest of the file
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; When we get AP items (4F or 50), dont add them to the inventory
; This can also be purposed for a custom items handler for consumables greater than 0x5F
@SpecialItemHandler:
    cmp r0, 3
    beq @@GiveSpecialWeapon ; Use this to check for the Vampire Killer
    cmp r0, 2
    bne @@End ; Items like this will only be normal pickups...
    cmp r1, 0x4F
    beq @@SkipItem
    cmp r1, 0x50
    beq @@SkipItem; 0x4F and 0x50 are used for offworld items...
    cmp r1, 0x5F
    bge @@CustomItemHandler ; Use this for custom, new items.
@@End:
    b 0x021E4428
@@SkipItem:
    bx lr ; Just don't do the give routine
@@CustomItemHandler:
    bx lr
@@GiveSpecialWeapon:
    cmp r1, 1 ; Standard vampire killer
    beq @@StandardVK
    cmp r1, 0x0A
    beq @@TrueVK
    b 0x021E4428
@@StandardVK:
    push r0-r2,lr
    mov r0, 3
    mov r1, 0x0A
    bl 0x021E45A4 ; Do we have the True VK?
    cmp r0, 0 ; If not...
    pop r0-r2, lr
    movne r0, 3
    movne r1, 0x0A ; If we already have the true VK, convert this item to the normal one
    movne r2, 1
    bne @SpecialItemHandler
    push r0-r2,lr
    mov r0, 3
    mov r1, 1
    bl 0x021E45A4 ; Do we already have a copy of the normal one?
    cmp r0, 0 ; If we do already have the normal VK, upgrade it!
    pop r0-r2, lr
    movne r0, 3
    movne r1, 0x0A
    movne r2, 1
    bne @SpecialItemHandler ; If we have the
    b 0x021E4428 ; Give the regular VK
@@TrueVK:
    push r0-r2,lr
    mov r0, 3
    mov r1, 1
    mov r2, 0
    bl 0x021E4428 ; Wipe out the standard VK no matter what
    ldr r0, =0x0211217C
    ldrb r1, [r0] ; Check Jonathans' current weapon
    cmp r1, 1 ; Is the normal VK equipped?
    bne @@SkipEquip
    mov r1, 0x0A
    strb r1,[r0] ; Replace with old one with the new one
@@SkipEquip:
    pop r0-r2, lr
    b 0x021E4428


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Clear out AP memory on a new file.
; Also, give the player a Magical Ticket to start with.
@InitializeNewGameData:
    push lr
    bl 0x021E4428
    mov r0, 2
    mov r1, 0x45
    mov r2, 1
    bl 0x021E4428 ; Give the player a magical ticket
    mov r0, 0x00 ; Clear
    ldr r1, =@ServerItemType
    mov r2, 0x50 ; 50 bytes
    bl 0x0209E570 ; Wipe the 0x50 bytes of AP memory when starting a new file
    ldr r0, =@OptionFlag_StartWithChangeCube
    ldrb r0, [r0]
    cmp r0, 0
    beq @@EndCubeCheck
    mov r0, 0
    mov r1, 1
    bl 0x02215308 ; Activate relic
    mov r0, 0x5C
    mov r1, 1
    bl 0x02215B2C ; Give the change cube
@@EndCubeCheck:
    ldr r0, = @OptionFlag_RevealMap
    ldrb r0,[r0]
    cmp r0, 0
    beq @@End
    ldr r0, =0x021119D0
    ldr r1, = 0xFFFFFFFF
    str r1,[r0] ; Set all of the Map bits, revealing the full map
@@End:
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;
@RamFlag_ItemColorOverride:
.db 0x00
.align 4


; Add a special handler to the DrawPopupWindow function
; We repoint to a new palette so I can add a new one
@ItemPalette_Cyan:
        .dh 0x0000
        .dh 0x0000
        .dh 0x014E
        .dh 0x0000
        .dh 0x1A32
        .dh 0x32D8
        .dh 0x573C
        .dh 0xFFFF
        .dh 0xFFFF
        .dh 0x7ECE
        .dh 0x0000
        .dh 0x0000
        .dh 0x65E6
        .dh 0x0000
        .dh 0x0000
        .dh 0x0000
@AddCyanPaletteToItemNames:
    cmp r0, 0x0E ; clearly oob so i use this for my stuff
    bne @@LoadNormalPalette
    ldr r5, = @ItemPalette_Cyan
    bx lr
@@LoadNormalPalette:
    add r5, r3, r0, lsl 0x05
    bx lr

; Use the Override color for item name displays, if one is present.
; This is used to change the color of AP items
@UseOverrideColor:
    ldr r0, = @RamFlag_ItemColorOverride
    ldrb r0, [r0] ; Is there an AP item primed?
    cmp r0, 0
    beq @@NormalColor
    push r0, r1
    ldr r0, =@RamFlag_ItemColorOverride
    mov r1, 0
    strb r1, [r0] ; Zero out the flag here
    pop r0, r1
    b 0x0204FEB4 ; We use our custom color instead
@@NormalColor:
    mov r0, 0x0A
    b 0x0204FEB4

; Use the item's flag as an index into the ItemColorTable
@LoadAPItemColor:
    ldrh r12, [r0, 0x3C] ; Get the flag val of the item
    push r0, r1
    ldr r0, = @ItemColorTable
    ldrb r0, [r0, r12]
    cmp r0, 0
    beq @@Skip
    ldr r1, = @RamFlag_ItemColorOverride
    strb r0, [r1] ; Store it for later

@@Skip:
    pop r0,r1
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;
;Stella's Locket is given to you in the cutscene, we handle it here instead
@GiveLocketItem:
    push r0-r2,lr
    bl 0x021D13EC ; Run the original code, runs end-of-battle cleanup on bosses
    ldr r2, = @RamFlag_ItemColorOverride
    ldr r1, = @StellaLocketItem
    ldrb r0, [r1, 2] ; Read the Item's Color
    strb r0,[r2] ; Transfer the item color so that we can use it if it's an ap item
    ldrb r0, [r1, 1] ; R0 = Item Type
    ldrb r1,[r1] ; R1 = Item ID
    cmp r0, 8
    beq @@LocketSkill
@@GiveLocketSkill:
    bl @GetItemArbitrary ; Pass off to the actual item routine
    ldr r0, =0x2111BE9
    ldrb r1,[r0]
    orr r1, r1,0x01
    strb r1,[r0] ; Write this Loc flag
    pop r0-r2,lr
    bx lr
@@LocketSkill:
    push r0,r1
    bl 0x0202C064  ; Stella's cutscene unloaded the font, so if we get a skill we need to reload it
    pop r0,r1
    b @@GiveLocketSkill
;;;;;;;;;;;;;;;;;;;;;;
; Normally this checks an event flag that Wind has been shown Stella's locket
; Instead, we only want to check that the item is owned
@CheckPresenceOfLocket:
    push lr
    mov r0, 7
    mov r1, 3 ; Load Stella's Locket
    bl 0x021E45A4 ; Check the item count
    cmp r0, 0
    pop lr
    bx lr

; This is the init for the cutscene when you haven't turned it in.
; Check if we have the locket, and cancel the cutscene if we do.
; This is to handle getting it while in the same room
@ForestPortraitSceneCheck:
    bl @CheckPresenceOfLocket
    bne @@EndForestScene
    mov r0, r4
    b 0x022EC8A4
@@EndForestScene:
    push r1
    ldr r0, = 0x02111BB1
    ldrb r1, [r0] ; Get the flag
    orr r1, r1, 0x0C ; Set the evnt flag that you've talked to wind about this
    strb r1, [r0]
    pop r1
    b 0x022EC87C ; Clean up and end the scene
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Prevent equipment from being applied on the glitchy character menus.
; This should patch out memory corruption
@DontEquipOnGlitchMenu:
    ldrsh r2,[r0,0xE4]
    cmp r2, 1
    bgt 0x0203B8DC
    b 0x0203B660
;;;;;;;;;;;;;;;
; Clamps position for the map, fixes suspend bug
@ClampXPosToRoomWidth:
  mov r0, r0, asr 14h ; Divide X by 0x100000 subpixels to get X in screens.
  cmp r0, 0h
  movlt r0, 0h ; X = 0 if X < 0
  ldr r2, =02112458h
  ldr r2, [r2]
  ldrb r2, [r2] ; Load the room's width from the collision layer (the first layer)
  sub r2, r2, 1h
  cmp r0, r2
  movgt r0, r2 ; X = room_width-1 if X > room_width-1
  bx r14
@ClampYPosToRoomHeight:
  ldr r12,=2AAAAAABh
  smull r12,r0,r12,r0 ; Divide Y in subpixels by 6
  mov r0, r0, asr 11h ; Further divide Y by 0x20000, divided by a total of 0xC0000 to get Y in screens
  cmp r0, 0h
  movlt r0, 0h ; Y = 0 if Y < 0
  ldr r2, =02112458h
  ldr r2, [r2]
  ldrb r2, [r2, 1h] ; Load the room's height from the collision layer (the first layer)
  sub r2, r2, 1h
  cmp r0, r2
  movgt r0, r2 ; Y = room_height-1 if Y > room_height-1
  bx r14
;;;;;;;;;;;;;;;;;;
; Switches the underground passage/nest of evil to check portraits instead of a flag
@Undergroundpassage_Portraitcheck:
    push lr
    bl @CheckPortraitClearCount
    ldr r1, = @OptionFlag_NestPortraits
    ldrb r1,[r1] ; Check the set number
    cmp r0, r1 ; If cleared portraits >= required
    mov r0, 0
    bge @@ActivateCheck
    cmp r0, 0
    pop lr
    bx lr
@@ActivateCheck:
    cmp r0, 1
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;
; Counts how many portraits have been cleared
@PortraitBossFlags:
    .db 0x01, 0x05, 0x06, 0x07, 0x8, 0x09, 0x0A, 0x0B
@CheckPortraitClearCount:
    push r1-r6
    ldr r1, =0x021119DC
    ldr r1,[r1] ; Load the bosses killed flags
    mov r0, 0
    mov r2, 0
    mov r6, 1
    ldr r3, =@PortraitBossFlags
@@Loop:
    ldrb r5, [r3,r2] ; Load the current flag
    lsl r5, r6, r5 ; Shift to get a bit
    ands r5, r5, r1 ; And this
    addne r0, r0, 1
    cmp r2, 7
    addne r2, r2, 1
    bne @@Loop
    pop r1-r6
    ;r0 = clear count
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;;;
; If Brauner Goal, teleport to ending.
; Else; teleport to portrait room
@PostBraunerCheck:
    push r0
    ldr r0, = 0x02111785
    ldrb r0, [r0] ; Get the current area
    cmp r0, 0x0B ; Are we in the Lost Galley?
    bne @@NormalPortrait
    pop r0
    ldr r0, = @OptionFlag_DraculaGoal
    ldrb r0, [r0]
    cmp r0, 1 ; Did the player choose Dracula goal?
    beq @@DraculaTeleport
    ldr r0, =0x021119DE
    ldrb r1, [r0]
    orr r1, r1, 0x02 ; Dracula
    strb r1,[r0] ; Set Dracula's defeat flag so the ending works
    mov r0, 0x0C
    mov r1, 0x00
    mov r2, 0x00
    mov r3, 0x00
    b 0x02032D90 ; Warp to the epilogue room
@@DraculaTeleport:
    mov r0, 0
    mov r1, 0x0B
    mov r2, 0x00
    mov r3, 0x100
    b 0x02032D90 ; Warp to the Portrait room, outside the studio portrait
@@NormalPortrait:
    pop r0
    b 0x02032D90 ; Do the normal warp instead of the special warp
;;;;;;;;;;;;;;;;;;;;;;;;;;;
@GetWhipMemItem:
    push r0-r2,lr
    ldr r2, = @RamFlag_ItemColorOverride
    ldr r1, = @WhipMemoryItem
    ldrb r0, [r1, 2] ; Read the Item's Color
    strb r0,[r2] ; Transfer the item color so that we can use it if it's an ap item
    ldrb r0, [r1, 1] ; R0 = Item Type
    ldrb r1,[r1] ; R1 = Item ID
    bl @GetItemArbitrary
    ldr r0, = 0x02111BB8
    ldrb r1,[r0]
    orr r1, r1, 0x80
    strb r1,[r0] ; Set the Loc flag for this check


    pop r0-r2,lr
    b 0x021CE664
;;;;;;;;;;;;;;;;;;;;;;;;;;;
;Move the Dracula flag to HERE so it doesn't go off mid-fight
@EndDracula:
    push r0,r1
    ldr r0, =0x021119DE
    ldrb r1,[r0]
    orr r1, r1, 0x02
    strb r1,[r0]
    pop r0,r1
    b 0x02032D90
;;;;;;;;;;;;;;;;;;;;;;;;
; Check the AP requirements for Dracula's barrier here
@CheckDraculaBarrierRequirements:
    push r0
    ldr r0, =@OptionFlag_DraculaGoal 
    ldrb r0,[r0]
    cmp r0, 0
    popeq r0
    beq 0x022E8894 ; If the goal is to fight Brauner, we don't want to access Dracula at all, so we bail

    push lr
    bl @CheckPortraitClearCount ; Grab the cleared portraits
    pop lr
    ldr r1, = @OptionFlag_DraculaPortraits ; and the required portraits
    ldrb r1, [r1]
    cmp r0, r1
    poplt r0
    blt 0x022E8894 ; If Cleared portraits < required, bail
    ldr r0, =@OptionFlag_DraculaRequirements
    ldrb r0,[r0]
    ands r0,r0, @OptionFlag_BraunerRequired
    beq @@SkipBraunerCheck ; If Brauner is not set as required, we can just skip this
    ldr r0, =0x021119DC
    ldr r0,[r0] ; Get the boss death flags
    ands r0, r0, 0x8000 ; Check Brauner's death flag
    popeq r0
    beq 0x022E8894 ; Brauner is required but not defeated, so bail  
@@SkipBraunerCheck:
    ldr r0, =@OptionFlag_DraculaRequirements
    ldrb r0,[r0]
    ands r0,r0, @OptionFlag_NestRequired
    beq @@SkipNestRequirement
    ldr r0, = 0x02111BC5
    ldrb r0,[r0]
    ands r0,r0,0x20 ; This is the pickup flag for the final item in Nest of Evil. All of its flags are otherwise temporary, so this is the closest we can get to a clear check
    popeq r0
    beq 0x022E8894
@@SkipNestRequirement:
    pop r0
    b 0x022E8884 ; All checks pass so delete the barrier
;;;;;;;;;;;;;;;;;;;;;;;;
; Checks the requirements to enter Brauner's portrait
@CheckBraunerRequirements:
    push lr
    bl @CheckPortraitClearCount
    pop lr
    ldr r1, = @OptionFlag_BraunerPortraits
    ldrb r1, [r1]
    cmp r0, r1 ; If we have cleared more than are required
    bge @@PortraitRequirementMet
    sub r0, r1, r0 ; Get the difference in portraits
    cmp r0, 4
    bge @@Draw4Chains
    mov r1, 1
    mov r1, r1, lsl r0
    sub r1, r1, 1
    strb r1, [r4,0x13C]
    b 0x02076BF4


@@PortraitRequirementMet:
    ldr r0, = @OptionFlag_DraculaGoal
    ldrb r0,[r0]
    cmp r0, 1
    beq 0x02076BF4 ; If Dracula is the goal, skip this and move on

    ldr r0, = @OptionFlag_DraculaRequirements
    ldrb r0,[r0]
    ands r0, r0, @OptionFlag_NestRequired
    cmp r0, 0
    beq 0x02076BF4 ; If Nest isn't required, don't check for it

    ldr r0, = 0x02111BC5
    ldrb r0,[r0]
    ands r0,r0,0x20 ; This is the pickup flag for the final item in Nest of Evil. All of its flags are otherwise temporary, so this is the closest we can get to a clear check
    bne 0x022E8894 ; If we've done it, just end
    mov r0, 1
    strb r0, [r4,0x13C] ; Store ONE chain as needing to be cleared
    b 0x02076BF4
@@Draw4Chains:
    mov r0, 0x0F
    strb r0, [r4,0x13C]
    b 0x02076BF4
;;;;;;;;;;;;;;;;
@ShowBreakableWalls:
    ldr r0, =@OptionFlag_RevealHiddenWalls
    ldrb r0,[r0]
    cmp r0, 0 ; the option is DISABLED
    beq @@CheckForDecay
    mov r0, 1
    bx lr
@@CheckForDecay:
    push lr
    mov r0, 3
    bl 0x02207C9C ; Check if Eye for Decay is equipped
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;;
; Vanilla quest rewards are bullshit.
;Instead, we do this-
@BetterQuestHandler:
    push r3
    push r0,r3
    ldr r3, = @RamFlag_SkipArbitrarayPopup
    mov r0, 1
    strb r0,[r3]
    pop r0,r3
    sub r3, r3, 4
    ldrh r3,[r3, r0]
    ands r1, r3, 0xFF ; Split this into item ID
    mov r0, r3, lsr 8 ; and item type
    bl @GetItemArbitrary
    ldr r3, = @RamFlag_SkipArbitrarayPopup
    mov r0, 0
    strb r0,[r3]
    pop r3
    b 0x02040844

    ;Convert the Reward text to get type/ID instead of global id
@GetQuestRewardText:
    push lr
    mov r0, r7, lsr 8 ; Funnel the TYPE into r0. the normal code does this by reverse ID searching
    mov r6,r0
    ands r1, r7, 0xFF
    cmp r0, 8
    bge @@GetQuestSkill
    cmp r0, 1
    beq @@GetQuestMoney
    bl 0x021E476C ; Get the global ID for this item
    mov r7, r0
    pop lr
    b 0x02040AF0
@@GetQuestSkill:
    pop lr
    mov r6, r0
    mov r7, r1
    mov r0, r1
    b 0x02040AF4
@@GetQuestMoney:
    pop lr
    mov r0, 0xB0
    add r1, r1, r0
    mov r6, 9
    mov r7, r1
    mov r0, r1
    b 0x02040AF4

    ;Same, but for the item description
@GetQuestRewardDesc:
    push lr
    mov r0, r6, lsr 8
    ands r1, r6, 0xFF
    cmp r0, 8
    bge @@GetQuestSkill
    cmp r0, 1
    beq @@GetQuestMoney
    bl 0x021E476C ; Get the global ID for this item
    mov r6, r0
    ldr r0, =0x151
    pop lr
    bx lr
@@GetQuestSkill:
    pop lr
    ldr r0, =0x151
    add r6, r0, r1
    bx lr
@@GetQuestMoney:
    pop lr
    ldr r1, = 0x051F
    b 0x02040D18



.pool

.endarea
.close