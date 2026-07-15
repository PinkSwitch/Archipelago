.nds
.relativeinclude on
.erroronwarning on

@Overlay86Start equ 0x022EB1A0
@FreeSpace equ @Overlay86Start + 0x60

@ReceivedItemID equ 0x022EB1B0 ; 2 bytes
@TotalItemsReceived equ 0x022EB1B2 ; 2 bytes

;;;;;;;;;;;;;;;;
.open "ftc/arm9.bin", 0x02000000
    .org 0x0204E55C
        bl @InitializeNewGameData

    .org 0x0204E34C
        nop ; Remove starting Lizard Tail

    .org 0x0204E358
        nop ; Remove starting Lizard Tail equip

    .org 0x0204E360
        nop ; Remove starting Glyph Union

    .org 0x0204E36C
        nop ; Remove starting Glyph Union

    .org 0x0206DE18
        bl @LogExtendedGlyph

    .org 0x0206DE58
        b @ResetExtendedGlyph

    .org 0x0206CE5C
        bl @SwapExtendedGlyphID

    .org 0x0206DBBC
        bl @SwapExtendedGlyphIDPart2

    .org 0x0206CEC4
        bl @SwapGlyphFile4

    .org 0x020635B0
        b @GiveExpandedItems

    .org 0x0206D9B8
        b @ShowExtendedGlyphName

    .org 0x02062E5C
        bl @ItemNameRedir ; Force item pickups to use the standardized method of showing their name

    .org 0x0209D170
        b @ShowExtendedItemNames

    .org 0x020378F0
        bl @GetRemoteItem

    .org 0x02037C10
        bl @LoadAPData

    .org 0x02062E7C
        bl @PlayProperPickupSound

    .org 0x0206D85C
        b @GlyphDelay

    .org 0x02063134
        b @ExpandedItem_SetAsConsumable

    .org 0x0209D774
        nop ; Prevent the game from trying to bail on getting expanded item pointer data

    .org 0x02063398
        b @ExpandedItemPointers

    .org 0x0206D9EC
        b @WriteExtendedGlyphName

    .org 0x020AD420
        bl @SaveAPData_Statue

    .org 0x020436E8
        bl @AutoMapReveal

    .org 0x0206DA54
        bl @SkipExcessGlyphItems

.close
;;;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_0", 0x021DD280
    .org 0x021E26BD
        .db 0x24, 0x49, 0x44, 0x00, 0x21, 0x4C, 0x42, 0x55, 0x53, 0x0E, 0x0E, 0x0E, 0xE6, 0x44, 0x4F ; Did Albus... do this?
        .db 0x00, 0x54, 0x48, 0x49, 0x53, 0x1F, 0xE6, 0xE5, 0xE4, 0xEA

    .org 0x021DE136
        .db 0x21, 0x30, 0x00, 0x29, 0x54, 0x45, 0x4D, 0xEA ; AP Item

    .org 0x021FB068
        .dw 0x021DE134 ; Pointers for the other 2 easter egg items to redirect to AP item
        .dw 0x021DE134

    .org 0x021E98A3
        .db 0x28, 0x41, 0x48, 0x41, 0x00, 0x59, 0x4F, 0x55, 0x00, 0x53, 0x48, 0x4F, 0x55, 0x4C, 0x44
        .db 0x00, 0x48, 0x41, 0x56, 0x45, 0x00, 0x46, 0x4F, 0x55, 0x4E, 0x44, 0x00, 0x11, 0x13, 0xE6
        .db 0x56, 0x49, 0x4C, 0x4C, 0x41, 0x47, 0x45, 0x52, 0x53, 0x0E, 0xE6, 0xE5, 0xE4, 0xEA ; Haha you should have found 13 villagers

    .org 0x021FAE60
        .dw @MapGlyph
        .dw @ProgGlyph
        .dw @UsefulGlyph
        .dw @FillerGlyph
        .dw @ItemGlyph
        .dw @MoneyGlyph
        .dw @VillagerGlyph

.close
;;;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_19", 0x021FFFC0
    .org 0x0221A670
        bl @ShowItemFromChest

    .org 0x0221ADFC
        b @SetChestColor

    .org 0x0221AEA4
        b @RevealBlueChests

    .org 0x0221D6C4
        b @UnlockItemFromAreaExit

    .org 0x0221F1A0
        bl @SetFireGlyph

    .org 0x0221A6B0
        bl @GetItemArbitrary
        b 0x0221A778

    .org 0x0221D7C8
        b 0x0221D7E8 ; prevent the game from trying to unlock areas normally on exit

    .org 0x0221D7F4
        b 0x0221D844 ; Prevent the game from trying to unlock extra areas on exit

    .org 0x0221A4A8
        bl @GetChestSprite

    .org 0x0221AFD8
        bl @MakeBlueChest

    .org 0x0221D6F4
        b @DelayAreaFade

    .org 0x0221D6B4
        b @CheckAreaDelay
.close
;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_20", 0x021FFFC0
    .org 0x02213F48
        b 0x02214090 ; Skip opening logos

    .org 0x02214340
        cmp r0, 1 ; Make the first opening movie fade faster

    .org 0x022143B8
        cmp r0, 0xFF ; Make the first opening switch to the title faster
        
.close
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_22", 02223E00h
    .org 0x0222949C
        nop ; Make magical tickets not get used up

    .org 0x02229884
        nop ; Allow ticket use before reaching the village

    .org 0x0223326C
        tst r0, 0x02 ; Nikolai's cutscene triggers on tutorial flags rather than the monastery flag
        b 0x02233298 ; Skip the first cutscene


    .org 0x022B5C18
        .db 0x08 ; Fix Nikolai's rescue flag

    .org 0x0223186C
        b @CheckVillagerLocFlag

    .org 0x0222EEC0
        b 0x0222EEDC ; Skips past a part that checks varB. I think this is being used for the bad ending otherwise.

    .org 0x02231B30
        bl @SetVillagerLocFlag

    .org 0x022318D8
        b @SpawnTrappedNikolai

    .org 0x0223329C
        b 0x022332D0 ; Spawns Nikolai in Wygol village. He's a normal object now, so we don't want this event one to spawn

    .org 0x02231A94
        .dw 0x67F ; Set George to have the proper text id

    .org 0x02230A84
        bl @AlbusEvntGlyphScene

    .org 0x0223778C
        b @BarloweEventHandler

    .org 0x02231F74
        nop ; Skip the bad ending fade in wait

    .org 0x02231FA4
        nop ; Skip the time we would normally hang on the villager

    .org 0x02231FF0
        nop
        bl @SkipBadEnding

    .org 0x02232118
        bl 0x0206EDDC ; Unequip Dominus Agony for the bad ending without removing it from the inventory

    .org 0x02231D14
        nop ; Remove the check to walk over to rescued villagers

    .org 0x02231D38
        mov r0, 2
        strb r0, [r6, 0x0D] ; Ignore the camera pan check for rescued villagers

    .org 0x02231ADC
        bl @VillagerSkipManager

    .org 0x02231AFC
        b @VillagerSkip_SetActive

    .org 0x022322D4
        bl @Villager_ResetEventData

    .org 0x022300EC
        b @CheckSpawningVillagerEvent

    .org 0x02231868
        bl @IsSpawningVillagerEvent

    .org 0x02237758
        b 0x02237784 ; Prevent Barlowe from playing the post-Oblivion Ridge event.

    .org 0x0222DAF4
        bl @SaveAPData_Suspend

    .org 0x0223208C
        ; bad ending
        bl @SaveAPData_Ending

    .org 0x0223B364
        ; good ending
        bl @SaveAPData_Ending

    .org 0x02297C7C
        bl @CheckBreakableWalls

    .org 0x022988D8
        bl @SetExtendedGlyphStatues  ; During creation, so it spawns the right object

    .org 0x0229858C
        bl @CheckExtendedStatueAsGlyph  ; General purpose. This tells if the statue spawns a glyph or not.

    .org 0x022984D0
        bl @CheckExtendedStatueAsGlyphParticle  ; This tells the statue to create the glyph particle effects

    .org 0x02298900
        bl @GetGlyphStatueFlag

    .org 0x0229890C ; Adds 1 to check the flag. We don't need this anymore
        mov r12, r2
    
    .org 0x022986A0
        bl @SetGlyphStatueFlag

    .org 0x0229A2B8
        bl @SpawnVillagerInWall

    .org 0x0223002C
        b @SetEventGlyphFlag

    .org 0x022376E0
        b 0x02237714  ; Part of Barlowe's initializer; prevent the game from using the post-Albus 1 Dialogue to skip the handler
        
.close
;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_28", 0x022B73A0
    .org 0x022B9690
        mov r0, 6  ; Wallman's Glyph flag

.close
;;;;;;;;;;;;;;;;;;;;;;

.open "ftc/overlay9_41", 0x022C1FE0
    .org 0x022C2754
        ; These are for Nikolai in wygol village
        mov r1, -1 ; Don't create the event actor for this

    .org 0x022C289C
        mov r1, -1 ; Set the camera focus to -1 as well

    .org 0x022C28C4
        mov r1, -1 ; Target for Shanoa to walk to

    .org 0x022C28F0
        mov r1, -1 ; And the focus for the second camera pan
.close
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_42", 0x022C1FE0

    .org 0x022D308D
        .db 0x00 ; Makes the hard-mode Glyph Sleeve chest always appear.

    .org 0x022C20C0
        b @GiveFirstGlyph

    .org 0x022C5A60
        bl @SpawnVillager

    .org 0x022C5568
        bl @FixBadEndingSkip

.close
;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_51", 0x022C1FE0
    .org 0x022C25EC
        bl @AlbusEvntGlyphSkip ; Minera prison

    .org 0x022C20E8
        bl @SetMineraAlbusGlyph

.close
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_52", 0x022C1Fe0
    .org 0x022C2490
        bl @SetStaticGlyph  ; Minera lightning room
.close
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_53", 0x022C1FE0
    .org 0x022C4894
        bl @SetStaticGlyph ; Lighthouse glyph
.close
;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_55", 0x022C1FE0
    .org 0x022C28E8
        bl @SetStaticGlyph ; Windy cave in Tymeo Mountains
.close
;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_57", 0x022C1FE0
    .org 0x022C230C
        bl @SetStaticGlyph_r5 ; Frozen Waterfall in Tristis Pass uses Object 0x47.

.close
;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_58", 0x022C1FE0
    .org 0x022C9094 ; Clear out the tunnel exiting Large Cavern
        .dh 0x4000

    .org 0x022C9096
        .dh 0x4000

    .org 0x022C9098
        .dh 0x4000

    .org 0x022C90B4
        .dh 0x4000

    .org 0x022C90B6
        .dh 0x4000

.close
;;;;;;;;;;;;;;;;;;;;;

.open "ftc/overlay9_59", 0x022C1FE0
    .org 0x022C25F0
        bl @AlbusEvntGlyphSkip ; Giant's dwelling

    .org 0x022C20E8
        bl @SetDwellingAlbusGlyph
.close
;;;;;;;;;;;;;;;;;;;;;


.open "ftc/overlay9_60", 0x022C1FE0
    .org 0x022C2FBC
        bl @SetStaticGlyph ; Dark room in mystery manor

    .org 0x022C29B8
        bl @AlbusEvent_CheckIfGlyphAbsorbed

    .org 0x022C2834
        nop ; Post-dominus villager check for the screen fade

    .org 0x022C2894
        nop ; post-dominus villager check for the cutscene proper

    .org 0x022C25BC
        bl @Albus3GlyphSpawn

    .org 0x022C25CC
        bl @SetManorAlbusGlyph ; Prevent r3 calculation & Set the flag for Albus 3's Glyph

    .org 0x022C2E4C
        bl @SetStaticChest  ; Sets an item for the dark room chest. Obj 54 VarA
.close
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_62", 0x022C1FE0
    .org 0x022C21A8
        bl @AlbusShowGlyphScene
.close
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_64", 0x022C1FE0
    .org 0x022C2054
        mov r1, -1 ; Don't spawn the George actor in skeleton cave

    .org 0x022C2180
        mov r1, -1 ; Camera focus

    .org 0x022C2528
        nop ; Prevent the game from spawning George's scene actor

.close
;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_72", 0x022C1FE0
    .org 0x022C2354
        bl @SetStaticGlyph ; generator puzzle in mechanical tower
.close
;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_78", 0x022C1FE0
    .org 0x022C31DC
        bl @SetCubusEvnGlyph

    .org 0x022C3224
        bl @SetStaticChest_cubes

    .org 0x022C2AD4
        bl @AlbusEvent_Monastery
.close
;;;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_86", @Overlay86Start
    .org @FreeSpace
    .area 0x32000
;Start of ROM data/variables
;022EB200
@AP_playerauth:  ; Reserve this space for AP connection data
    .fill 0x20

;Patch starts at 0x022EB220
@GenerationFlags:
    @OptionFlag_RevealHiddenChests: ;022EB220
        .db 0x01
    @OptionFlag_StartingArea: ;022EB221
        .db 0x12
    @OptionFlag_StartingItems: ; 022EB222
        .db 0x03 ; Bit 1 for Lizard Tail, Bit 2 for Glyph Union, bit 3 for GLyph Sleeve
    @OptionFlag_RevealHiddenWalls: ; 022EB223
        .db 0x00
    @RomVar_FireGlyph: ; 022EB224
        .dh 0x0032
    @OptionFlag_RequiredVillagers: ;022EB226
        .db 0x0D, 0x00
        .dh 0x00 ; Filler
    @OptionFlag_StartingVillagers: ;022EB22A
        .dh 0x0000
        .dh 0x0000
    @OptionFlag_RevealMap: ;022EB22E
        .db 0x00
    @OptionFlag_EXPMult:
        .dh 0x00 ; 022EB22F
.align 4

;;;;;;;;;;;;;;;;;;;;;;;;;;
; Allows Glyphs to be shown when opening a chest
@ShowItemFromChest:
    cmp r3, 0x70 ; Check if this is an Item
    blt 0x0206DDEC ; Glyphs have a different spawn fucntion, so we need to use it instead
    b 0x02063858 ; If it is an item, create it as normal
;;;;;;;;;;;;;;;;;;;;;;;;;
;Sets Glyphs and Progression items to use gold chests
@SetChestColor:
    push lr
    bl @GetChestColor
    cmp r0, 0xFF
    movge r0, 0
    pop lr
    strh r0, [r4, 0x8A]
    b 0x0221AE0C
;;;;;;;;;;;;;;;;;;;;;;;;;
; Sets blue chests to alwyas be visible
@RevealBlueChests:
    push r0
    ldr r0, =@OptionFlag_RevealHiddenChests
    ldrb r0, [r0]
    cmp r0, 0
    pop r0
    beq @@HideChest
    mov r0, 0
    cmp r0, 1
    b 0x0221AEC0
@@HideChest:
    cmp r0, 0
    b 0x0221AEA8
;;;;;;;;;;;;;;;;;;;;;;;;;
; Replaces the starting Albus event with one that gives you your starting glyph
@GiveFirstGlyph:
    push r0
    ldr r0, =0x02100388
    ldr r0, [r0] ; Get event flags
    ands r1, r0, 0x2 ; Intro event
    movne r0, r2
    popne r0
    bne 0x022C20DC
    orr r0, r0, 0x02
    ldr r1, =0x02100388
    str r0, [r1] ; Set the event flag for this so it doesnt happen again
    mov r0, 5
    mov r1, 1
    mov r2, 1
    bl 0x020657F8 ; Set the top screen to be the map
    push r1
    ldr r0, = 0x0004EBA0
    ldr r1, =0x02109850
    str r0, [r1]  ; Player's X pos
    ldr r0, = 0x0022F000
    str r0, [r1, 4] ; Y pos
    add r0, r4, 0x100
    ldrh r0, [r0, 0x3E] ; Use VarB as Glyph ID
    ldr r1, = 0x021002C0
    ;sub r0, r0, 1
    ;strh r0, [r1] ; Set the Starting Glyph as equipped
    ;strh r0, [r1, 2]
    ;add r1, r1, 0x12
    ;strh r0, [r1] ; Set the Starting Glyph as equipped in the menu
    ;strh r0, [r1, 2]

    bl @GetItemArbitrary
    pop r1
    pop r0
    b 0x022C20DC
;;;;;;;;;;;;;;;;;;;;;;;;;
; Automatically handles obtaining and displaying items.
@GetItemArbitrary:
    push r0-r5,lr
    cmp r0, 0x80
    blt @@SkipMax
    cmp r0, 0x82
    bgt @@SkipMax
    bl 0x02063EAC
    b @@SkipGivingItem
@@SkipMax:
    push r0
    bl 0x02063804 ; Convert item ID to a name
    mov r1, 0
    bl 0x0209D170 ; Display the item
    pop r0
    push r0
    bl @GetGlyphEXP
    bl 0x020635A4 ; Give the player the item in question
    pop r0
    bl @PlayItemSounds
@@SkipGivingItem:
    pop r0-r5,lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;;
; Sets up starting inventory and flags
@StartingRelics:
.db 0x70, 0x73, 0x74
.align 4
@InitializeNewGameData:
    push lr
    bl 0x0204E328 ; Set all of the regular stuff
    mov r0, 0x7C + 1
    bl 0x020635A4 ; Give the player a Magical Ticket
    mov r0, 0x3C
    ldr r1, =0x02100388
    strb r0, [r1] ; Set event flags for being past the intro
    mov r0, 1
    mov r1, 1
    bl 0x020AA95C ; Set Wygol village as unlocked
    ldr r0, =@OptionFlag_StartingArea
    ldrb r0, [r0]
    cmp r0, 0
    beq @@SkipAreaUnlock
    mov r1, 1
    bl 0x020AA95C
@@SkipAreaUnlock:
    push r2,r3
    mov r3, 0
    mov r2, 1
@@StartingRelicLoop:
    ldr r0, =@OptionFlag_StartingItems
    ldrb r1, [r0]
    tst r1, r2
    bne @@ActivateRelic
@@CheckEndLoop:
    add r3, 1
    cmp r3, 3
    beq @@End
    lsl r2, r2, 1
    b @@StartingRelicLoop
@@End:
    bl @GetStartingVillagers
    pop r2,r3
    pop lr
    bx lr
@@ActivateRelic:
    push r2, r3
    ldr r0, =@StartingRelics
    ldrb r0, [r0, r3]
    push r0
    mov r1, 1
    bl 0x020637C8 ; Activate the relic
    pop r0
    bl 0x020635A4
    pop r2, r3
    b @@CheckEndLoop
;;;;;;;;;;;;;;;;;;;;
; Forces Villagers to despawn based on VarB loc flag instead of their Event flag
@CheckVillagerLocFlag:
    push r0
    add r0, r4, 0x100
    ldrh r0, [r0, 0x3E] ; VarB
    bl @CheckLocFlag
    cmp r0, 0
    pop r0
    beq 0x02231884
    b 0x02231874


; Sets the location flag when rescuing a villager; does not override the Rescue flag
@SetVillagerLocFlag:
    push r12, lr
    add r0, r6, 0x100
    ldrh r0, [r0, 0x3E] ; Grab the VarB
    mov r1, 8
    bl 0x02023E68 ; Divide by 8
    mov r2, 1
    lsl r1, r2, r1 ;Shift to get the bit 
    ldr r2, =0x02100398 ; Flag table
    add r2, r2, r0
    ldrb r0, [r2]
    orr r0, r0, r1 ; Set the flag for this check
    strb r0, [r2]
    ldr r1, [r4, 0x158]
    pop r12, lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;
; Nikolai doesn't have proper trapped behavior, so we add it here
@SpawnTrappedNikolai:
    cmp r0, 0x08 ; Nikolai's trapped flag
    beq @@SetNikolai
    cmp r0, 0x40
    b 0x022318DC
@@SetNikolai:
    mov r5, 0x03 ; Nikolai's NPC id
    ldr r6, =0x676 ; Nikolai's rescued text
    b 0x022319CC

; Forces the camera for the Wygol cutscene to focus on object 0x10 instead of Nikolai specifically
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Give the player whatever item is on a given area exit.
; VarA - the Item ID
; VarB - the loc ID
@RamFlag_AreaExitDelay:
    .dh 0x0000
.align 4
@UnlockItemFromAreaExit:
    push r7
    add r7, r7, 0x100
    ldrh r0, [r7, 0x3C]
    cmp r0, 0
    beq @@Exit ; If no item is set, skip the item logic
    push r0-r5,lr
    ldrh r0, [r7, 0x3E]
    bl @CheckLocFlag ; Check if we've already activated this location
    cmp r0, 1
    popeq r0-r5,lr
    beq @@Exit ; If we HAVE already done this check, don't give its item again.
    ldrh r0, [r7, 0x3C]
    cmp r0, 0x70
    blt @@SkipDelay  ; Glyphs already pause the screen to show their item, so we dont' need to delay for them
    ldr r1, = @RamFlag_AreaExitDelay
    push r0
    mov r0, 0x5A
    strh r0, [r1]
    pop r0
@@SkipDelay:
    bl @GetItemArbitrary ; Use VarA as the Item ID to get.
    ldrh r0, [r7, 0x3E]
    bl @SetLocFlag ; Activate the flag so we don't do this again.
    pop r0-r5,lr
    pop r7
    b 0x0221D89C ; Bail. Don't continue logic yet.
@@Exit:
    pop r7
    mov r4, 1
    b 0x0221D6C8

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Checks r0 location flag. if set, returns 1, else 0
@CheckLocFlag:
    push r1-r2,lr
    mov r1, 8
    bl 0x02023E68
    ldr r2, =0x02100398
    add r2, r2, r0
    ldrb r0, [r2]
    mov r2, 1
    lsl r1, r2, r1
    tst r0, r1
    movne r0, 1
    moveq r0, 0
    pop r1-r2,lr
    bx lr

; Sets r0 Location Flag.
@SetLocFlag:
    push r1-r3,lr
    mov r1, 8
    bl 0x02023E68
    ldr r2, =0x02100398
    add r2, r2, r0
    ldrb r0, [r2]
    mov r3, 1
    lsl r1, r3, r1
    orr r0, r0, r1
    strb r0, [r2]
    pop r1-r3,lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;;;
@RamFlag_ExtendedGlyphID:
    .dh 0x00
.align 4

; Store extended Glyph ID
@LogExtendedGlyph:
    cmp r0, 0x6F
    blt @@LoadNormalGlyph
    push r1
    ldr r1, =@RamFlag_ExtendedGlyphID
    strh r0, [r1]
    pop r1
@@LoadNormalGlyph:
    b 0x0206CE4C

; Zeroes out the glyph flag
@ResetExtendedGlyph:
    bl 0x0206DBA4
    push r0, r1
    ldr r0, =@RamFlag_ExtendedGlyphID
    mov r1, 0
    strh r1, [r0]
    ldr r0 , = 0x656E7572
    ldr r1, = 0x020E50F8
    str r0, [r1] ; Set the rune file back in place
    pop r0,r1
    b 0x0206DE5C

; If the Extended flag ID is set, override the ID of whatever this Icon was
@SwapExtendedGlyphID:
    ldr r0, =@RamFlag_ExtendedGlyphID
    ldrh r0, [r0]
    cmp r0, 0
    beq @@Exit
    push lr
    bl @GetExtendedGlyphNum
    pop lr
    mov r1, r0
@@Exit:
    mov r0, r1, asr 3
    bx lr
.pool

;Same as the above but in the compare no load function
@SwapExtendedGlyphIDPart2:
    ldr r0, =@RamFlag_ExtendedGlyphID
    ldrh r0, [r0]
    cmp r0, 0
    beq @@Exit
    push lr
    bl @GetExtendedGlyphNum
    pop lr
    mov r5, r0
@@Exit:
    mov r0, r5, asr 3
    bx lr

; Switches out Rune4 with fSha4
@SwapGlyphFile4:
    push r0,r1
    ldr r0, =@RamFlag_ExtendedGlyphID
    ldrh r0, [r0]
    cmp r0, 0
    beq @@End
    ldr r1, =0x61687366 ;Fsha04
    ldr r0, =0x020E50F8 ; Overwrite rune04
    str r1, [r0]
@@End:
    pop r0,r1
    b 0x02033048

@GetExtendedGlyphNum:
    cmp r0, 0xD6
    moveq r0, 0x43 ; AP prog 
    bxeq lr
    cmp r0, 0xD4
    moveq r0, 0x42
    bxeq lr
    cmp r0, 0x160
    bgt @@ExpandedItems
    mov r0, 0x41 ; Regular items
    bx lr
    ; Custom items here
@@ExpandedItems:
    sub r0, r0, 1
    sub r0, r0, 0x160
    cmp r0, 0x07
    movlt r0, 0x44 ; Money glyphs
    bxlt lr
    cmp r0, 0x15
    movge r0, 0x45 ; Maps
    bxge lr
    mov r0, 0x40; villagers
    bx lr
;;;;;;;;;;;;;;;;;;;;
; Gives expanded Item IDs properly.
; 0x161-167- Money
; 168-175 ; Villagers
; Maps, 176
;push lr
@MoneyValues:
.dh 0x01, 0x0A, 0x32, 0x64, 0x1F4, 0x3E8, 0x7D0
.align 4
@GiveExpandedItems:
    cmp r0, 0x160
    bgt @@ExpandedItem
    b @@NormalItem
@@ExpandedItem:
    sub r0, r0, 1
    sub r0, r0, 0x160
    cmp r0, 7
    blt @@GetMoney
    cmp r0, 0x15
    bge @@GetMap
    b @@GetVillager
@@NormalItem:
    cmp r0, 0x70
    blt @@EndNormal ; Glyphs
    cmp r0, 0x75
    bgt @@APItemCheck ; Regular items
    bl @ActivateNewRelic
@@EndNormal:
    bl 0x020633F0
    b 0x020635B4
@@GetMap:
    sub r0, r0, 0x15
    mov r1, 1
    cmp r0, 0x06 ; Kalidus channel
    beq @@CheckKalidusUnlock
@@UnlockKalidus1:
    bl 0x020AA95C
    b @@End
@@GetMoney:
    push r2
    ldr r2, =@MoneyValues
    mov r0, r0, lsl 1
    ldrh r0, [r2, r0] ; Get the money amnt
    ldr r1, = 0x2100310 ; Money
    ldr r2, [r1]
    add r0, r2, r0
    str r0, [r1]
    pop r2
    b @@End
@@GetVillager:
    sub r0, 0x07
    bl @UnlockVillager
    mov r0, 0x1F
    bl 0x020635A4 ; Give the player a free Torpor when they unlock any villager
    b @@End
@@End:
    b 0x02063634
@@CheckKalidusUnlock:
    push r0
    bl 0x020AA94C ; Check if we've already unlocked Kalidus
    tst r0, 2
    pop r0
    moveq r1, 1
    beq @@UnlockKalidus1 ; We have NOT be en to Kalidus yet, so just unlock the area normally
    mov r1, 0x01
    mov r2, 0x09
    bl 0x02046144 ; Mark the area for the bottom exit as explored
    mov r0, 0x6
    mov r1, 0x0
    mov r2, 0x0
    bl 0x02046144 ; Mark the area for the top exit as explored so we can go back there
    b @@End
@@APItemCheck:
    cmp r0, 0xD4
    blt @@EndNormal
    cmp r0, 0xD6
    bgt @@EndNormal
    b @@End ; If it's an AP item, skip giving it to the player at all.

;;;;;;;;;;;;;;;;;;
; Shows item names for non-glyph gylphs.
; Uses ShowItemName for this as well.
@ShowExtendedGlyphName:
    cmp r0, 0x70
    blt @@ShowGlyphNormal
    b 0x0206D9C4 ; We want to always show a big popup if it's an Item glyph
@@ShowGlyphNormal:
    bl 0x020633F0
    b 0x0206D9BC
;;;;;;;;;;;;;;;;
@ShowExtendedItemNames:
    sub r0, r0, 0x15 ; Subtract text index to get the item's ID
    push r3, lr
    cmp r0, 0x76
    blt @@ShowSpecialName
    cmp r0, 0x160
    bgt @@ShowExpandedNames
@@ItemDisplay:
    add r0, r0, 0x15
@@NameDisplay:
    b 0x0209D174
    pop lr
@@ShowSpecialName:
; Used for Glyphs and Relics
    push r0
    bl 0x020633F0 ; Check the amount of this item we own
    cmp r0, 0
    pop r0
    bne @@ItemDisplay ; If we already own one of this item, show it as a standard popup
    push r0-r4
    mov r4, r0
    add r2, r0, 0x178
    sub r2, r2, 1
    mov r0, 0x50
    mov r3, 0
    mov r1, 0x32
    str r3, [r13]
    bl 0x0209D0D0
    mov r1, r4
    bl 0x0209D130
    pop r0-r4
    b 0x0209D19C
@@ShowExpandedNames:
    sub r0, r0, 1
    sub r0, r0, 0x160
    cmp r0, 0x07
    bge @@ShowVillager
    lsl r0, r0, 1
    ldr r2, =@MoneyValues
    ldrh r0, [r2, r0]
    mov r1, 1

    b @@NameDisplay
@@ShowVillager:
    cmp r0, 0x15
    bge @@ShowAreaName
    sub r0, r0, 0x07
    add r0, r0, 0x03 ;Villager name text
    b @@NameDisplay
@@ShowAreaName:
    sub r0, r0, 0x15
    add r0, r0, 0x5A0
    add r0, r0, 1
    b @@NameDisplay
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
@ActivateNewRelic:
    push lr
    push r0
    bl 0x020633F0 ; Check if we already owned this relic
    cmp r0, 0
    pop r0
    bne @@End
    push r0,r1
    mov r1, 1
    bl 0x020637C8 ; Activate the relic
    pop r0, r1
@@End:
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Spawns the new Glyph for Cubus. uses the block object's VarB
@SetCubusEvnGlyph:
    add r3, r8, 0x100
    ldrh r3, [r3, 0x3E] ; VarB
    bx lr

; Spawns Glyphs that are created as part of other objects. Lighthouse, umbra, etc.
@SetStaticGlyph:
    add r3, r4, 0x100
    ldrh r3, [r3, 0x3E] ; VarB
    bx lr

; Spawns Glyphs that are created as part of other objects. Lighthouse, umbra, etc.
@SetStaticGlyph_r5:
    add r3, r5, 0x100
    ldrh r3, [r3, 0x3E] ; VarB
    bx lr

;;;;;;;;;;;;;;;;;;;;;
; Spawns the new Glyph for Albus's event. This is the glyph as spawned when skipped.
@AlbusEvntGlyphSkip:
    str r12, [r13]
    add r1, r4, 0x100
    ldrh r1, [r1, 0x3E] ; Use VarB for the Glyph
    ldr r2, =0xFFFFFFE8
    ldr r3, =0xFFFFFFC0 ; Position for the glyph?
    bx lr

; Spawns Albus's event glyph during the cutscene when he holds it out
@AlbusEvntGlyphScene:
    ldr r6, =0x0210D180
    ldrh r6, [r6, 0x3E] ; VarB
    bx lr

@AlbusShowGlyphScene:
    add r3, r5, 0x100
    ldrh r3, [r3, 0x3E]
    b 0x0206DDEC

; An override to make sure we've absorbed the glyph in Mystery Manor before continuing that scene.
@AlbusEvent_CheckIfGlyphAbsorbed:
    push r0
    ldr r0, =0x02100388
    ldr r0, [r0] ; event flags
    tst r0, 0x00400000 ; Dominus 3 absorbed
    pop r0
    beq @@DespawnEvent
    b 0x0222EE20
@@DespawnEvent:
    mov r0, 0
    bx lr

@Albus3GlyphSpawn:
    ldr r1, =0x0210D180
    ldrh r1, [r1, 0x3E] ; VarB
    ldr r3, =0xFFFFFFBF
    bx lr

; We can't change the Vars for vol ignis, so just use an override for it...
@SetFireGlyph:
    ldr r3, =@RomVar_FireGlyph
    ldrh r3, [r3]
    bx lr
;;;;;;;;;;;;;;;;;;;;
; Activates Albus's Monastery check. VarB is the item ID
@AlbusEvent_Monastery:
    push lr
    add r0, r5, 0x100
    ldrh r0, [r0, 0x3E] ; VarB
    bl @GetItemArbitrary
    mov r0, 0xC5
    bl @SetLocFlag ; Set a location flag saying we've been here
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;;
; Remote Item Handler; gives the player an item
@GetRemoteItem:
    ldr r0, =0x020FFC8C ; Global game flags
    ldr r0, [r0]
    tst r0, 0x88000001 ; Filter popups, the pause menu, and Events
    bne @@Exit
    tst r0, 0x000000C0 ; Filter death, HUD hider
    bne @@Exit
    tst r0, 0x00100000 ; Filter for room transition
    bne @@Exit
    ldr r0, =0x02159A3A ; Text popup timer
    ldrb r0, [r0]
    cmp r0, 0
    bne @@Exit ; We don't want to get items while there's a text-popup up
    ldr r0, =0x02100A9E ; Some sort of fade value
    ldrb r0, [r0]
    cmp r0, 0
    bne @@Exit ; Don't want to get items while the screen isn't fully visible
    ldr r0, =@ReceivedItemID
    ldrh r0, [r0] ; Current received item
    cmp r0, 0
    beq @@Exit ; We haven't received any item
    push lr
    bl @GetItemArbitrary
    pop lr
    ldr r0, =@ReceivedItemID
    mov r1, 0
    strh r1, [r0] ; Zero out the item after receiving it
@@Exit:
    b 0x02037FCC
;;;;;;;;;;;;;;;;;;;;
; Plays the sound effect for picking up a specific item
@PlayItemSounds:
    push lr
    bl @GetPickupSound
    bl 0x020AA4D4 ; Play the sound
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;
; Reset var1 to 0 for pickups on the ground
@ItemNameRedir:
    mov r1, 0 ; Reset the item name var
    b 0x0209D170
;;;;;;;;;;;;;;;;;;;;;
; Sets r0 Villager's unlock flag
@UnlockVillager:
    push r0-r5,lr
    ldr r1, =0x022B5C10 ; Villager data
    add r1, r1, 8
    mov r2, 10
    mul r0, r0, r2
    add r1, r1, r0
    ldrb r0, [r1]


    mov r1, 8
    bl 0x02023E68
    ldr r2, =0x02100388
    add r2, r2, r0
    mov r0, 1
    lsl r0, r0, r1
    ldrb r1, [r2]
    orr r0, r0, r1
    strb r0, [r2]
    pop r0-r5,lr
    bx lr
;;;;;;;;;;;;;;;;;;;;
; Handles Ecclesia events
@BarloweEventHandler:
    ldr r0, =0x02100388
    ldr r0, [r0]
    tst r0, 0x04000000 ; Don't check this if we've already dealt with Barlowe.
    movne r0, 0
    bne 0x022377C4
    mov r0, 0x32 ; Dominus Hatred
    bl 0x020633F0
    cmp r0, 0
    beq 0x022377C4
    mov r0, 0x33 ; Dominus Anger
    bl 0x020633F0
    cmp r0, 0
    beq 0x022377C4
    mov r0, 0x4F ; Dominus Agony
    bl 0x020633F0
    cmp r0, 0
    beq 0x022377C4 ; We want to check that the player has all 3 Dominus + Glyph Union before proceeding, instead of the Albus flag
    ; We know the player has all of Dominus + Union, so check the bad ending next
    bl 0x0223488C ; Check the villagers
    ldr r1, =@OptionFlag_RequiredVillagers
    ldrb r1, [r1]
    cmp r0, r1
    blt @@BadEndingCheck 
    b 0x0223780C  ; If the player has all 3 Dominus, and the right amount of villagers, start Barlowe's fight
@@BadEndingCheck:
    mov r0, 0x73 
    bl 0x020633F0  ; If we're triggering the bad ending, we want to check that the player has Glyph Union so that they don't get softlocked
    cmp r0, 0
    beq 0x022377C4
    b 0x0223779C ; Trigger the ending
;;;;;;;;;;;;;;;;;;;;;;
; Skips the villager runthrough after getting the Bad Ending.
@SkipBadEnding:
    push lr
    mov r0, 4
    mov r1, 1
    mov r2, 1
    bl 0x020657F8 ; Set the top screen back to the cross
    mov r0, 0
    pop lr
    bx lr

; We spawn a generic villager object so that the Bad Ending still triggers properly
@SpawnVillager:
    push lr
    ldr r0, = 0x020FFC8C
    ldr r1, [r0]
    orr r1, r1, 0x80000000 ; Set the Event flag
    orr r1, r1, 0x00100000 ; Set the NoMove flag
    str r1, [r0]
    add r1, r5, 0x100
    mov r2, 0x2D
    mov r0, r5
    strh r2, [r1, 0x3C]
    mov r2, 0
    strh r0, [r1, 0x3E] ; 0 out VarB so it doesn't read as a loc flag
    bl 0x0223183C ; Spawn the villager
    ldr r0, =0x02231ABC ; ...And set their Update code
    str r0, [r5]
    pop lr
    bx lr

; My bad ending changes would otherwise allow the scene to be skippable after watching it
@FixBadEndingSkip:
    push r4,lr
    ldrb r4, [r5, 0x0D]
    cmp r4, 0x0A
    bge @@DisallowSkip
    ldr r4, [r5, 0x158]
    bl 0x0222F038
    @@DisallowSkip:
    pop r4,lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Save statue handler
@SaveAPData_Statue:
    push lr
    bl @SaveAPData
    pop lr
    b 0x02008CD4

;Suspend handler
@SaveAPData_Suspend:
    push lr
    bl @SaveAPData
    pop lr
    b 0x020891FC

;ending handler
@SaveAPData_Ending:
    push lr
    bl @SaveAPData
    pop lr
    b 0x0209C9E4


; Copies data from the AP data struct into the save file for save handling
@SaveAPData:
    push lr
    push r0-r3,r12
    ldr r0, =@ReceivedItemID ; AP Data Block
    ldr r1, =0x02100590
    mov r2, 0x20
    bl 0x02008CD4
    pop r0-r3,r12
    pop lr
    bx lr

; Copies data back from the save struct into the AP data
@LoadAPData:
    push lr
    push r0-r3,r12
    ldr r0, =0x02100590 ; AP Data Block
    ldr r1, =@ReceivedItemID
    mov r2, 0x20
    bl 0x02008CD4
    pop r0-r3,r12
    pop lr
    b 0x0204E4B8
;;;;;;;;;;;;;;;;;;;;;;;
; Plays the important sfx for Relics on freestanding pickups
@PlayProperPickupSound:
    push lr
    ldr r0, [r4, 0xE0] ; Item ID
    bl @GetPickupSound
    pop lr
    bx lr

; Returns the SFX ID for r0 item ID
@GetPickupSound:
    push r1
    mov r1, r0
    ldr r0, = 0x41A10000 ; Volume
    cmp r1, 0x70
    blt @@GlyphSound
    cmp r1, 0x76
    blt @@RelicSound
    cmp r1, 0x160
    bgt @@ExpandedItems
    b @@ItemSound
@@ExpandedItems:
    sub r1, r1, 1
    sub r1, r1, 0x160
    cmp r1, 0x07
    bge @@ItemSound ; Non-money mains
    mov r1, 0x0D ;Money
    ldr r0, =0x11A00000
    b @@Return
@@GlyphSound:
    mov r1, 0x07
    b @@Return
@@RelicSound:
    mov r1, 0x03
    b @@Return
@@ItemSound:
    ldr r0, =0x11A00000
    mov r1, 0x0C
    b @@Return
@@Return:
    add r0, r0, r1
    pop r1
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;
; Prevents excess cutscene skipping on villagers so as not to break them.
@RamFlag_ActiveVillagerObj:
    .dw 0x0000
@VillagerSkipManager:
    ldr r0, =@RamFlag_ActiveVillagerObj
    ldr r0, [r0]
    cmp r0, 0 ; if nothing is active, ignore this
    beq @@End
    cmp r6, r0
    beq @@End ; If the current active Object is the one for this scene, check skips as normal
    mov r0, 0
    bx lr ; Otherwise, end early
@@End:
    mov r0, r6
    b 0x0222F038

; Sets the current villager object as the one we're focusing on
@VillagerSkip_SetActive:
    push r0
    ldr r0, =@RamFlag_ActiveVillagerObj
    str r6, [r0]
    pop r0
    b 0x02231CCC

; Clears out local data that we set for the villager's cutscene
@Villager_ResetEventData:
    ldr r1, =@RamFlag_ActiveVillagerObj
    str r2, [r1] ; Clear out the currently active villager
    mov r1, 5
    b 0x0222F2D0
;;;;;;;;;;;;;;;;;;;;;
; Delays collecting Glyphs
@RamFlag_HasGottenGlyph:
    .db 0x00
.align 4
@GlyphDelay:
    push r0,r1
    ldr r0, [r5, 0xDC]
    bl @CheckLocFlag
    ldr r1, =@RamFlag_GlyphUnlocked
    strb r0, [r1]
    ldr r0, =@RamFlag_HasGottenGlyph
    ldrb r1, [r0]
    cmp r1, 0
    beq @@GetGlyph
    cmp r1, 2
    beq @@Reset
    add r1,r1, 1
    strb r1, [r0]
    pop r0,r1
    b 0x0206DB40
@@Reset:
    mov r1, 0
    strb r1, [r0]
    pop r0,r1
    b 0x0206DB40
@@GetGlyph:
    add r1, r1, 1
    strb r1, [r0]
    pop r0,r1
    ldr r14, [r4, 0x348]
    b 0x0206D860
;;;;;;;;;;;;;;;;;;;;;;;;
;Returns item type X for Expanded items.
@ExpandedItem_SetAsConsumable:
    cmp r0, 0x160
    movgt r4, 5
    bgt 0x02063214
    cmp r0, 1
    b 0x02063138

; Swaps out the Pointers for extended items, for chest GFX currently
@ExtendedPointer_Money:
    .dh 0
    .dh 0x280C
    .dw 0
    .db 8
    .db 9
    .dh 0
@ExtendedPointer_Villager:
    .dh 0
    .dh 0x300B
    .dw 0
    .db 8
    .db 9
    .dh 0
;;;;;;;;;;;;;
@ExpandedItemPointers:
    cmp r0, 0x160
    bgt @@GetExtraData
    mov r5, r0
    b 0x0206339C
@@GetExtraData:
    sub r0, r0, 1
    sub r0, r0, 0x160
    cmp r0, 0x07
    blt @@MoneyPtr
    cmp r0, 0x15
    blt @@VillagerPtr
    ldr r0, =0x020F051C ; use Magical Ticket for maps
    b 0x020633B8
@@MoneyPtr:
    ldr r0, =@ExtendedPointer_Money
    b 0x020633B8
@@VillagerPtr:
    ldr r0, =@ExtendedPointer_Villager
    b 0x020633B8
;;;;;;;;;;;;;;;;;;;
; Based on Glyph r0, gives Summon EXP
@GetGlyphEXP:
    push r0,lr
    cmp r0, 0x48
    blt @@end
    cmp r0, 0x4E
    bgt @@End; We only want to give EXP for Summons
    mov r1, 0x7D0
    bl 0x0206F028 ; Give EXP for the summon
    cmp r0, 0 ; Check if we leveled up
    beq @@End
    bl 0x0206DA30 ; Level up the Summon if necessary
    mov r0, 0x0A
    bl 0x020AD790
    cmp r0, 0
    bne @@End
    mov r0, 0x0A
    bl 0x020AD764
@@End:
    pop r0,lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;;
@RamFlag_VillagerSpawn:
    .db 0x00
.align 4
; Set a flag that we're spawning a villager so that the Glyphs don't override their events...
@IsSpawningVillagerEvent:
    push lr
    push r0,r1
    ldr r0, =@RamFlag_VillagerSpawn
    mov r1, 1
    strb r1, [r0]
    pop r0, r1
    bl 0x0222EE20
    pop lr
    push r0,r1
    ldr r0, =@RamFlag_VillagerSpawn
    mov r1, 0
    strb r1, [r0]
    pop r0,r1
    bx lr

; This clears out some meory for Events. This happens to override Villager stuff when multiple are in a room
; so we need it to NOT do that.
@CheckSpawningVillagerEvent:
    push r0,r1
    ldr r0, =@RamFlag_VillagerSpawn
    ldrb r1, [r0]
    cmp r1, 0
    beq @@End
    pop r0,r1
    b 0x022300F0
@@End:
    pop r0,r1
    str r1, [r0, r2, lsl 2]
    b 0x022300F0
;;;;;;;;;;;;;;;;;;;;;
; Returns the proper color of a chest for r0 item ID.
; FF - Brown
; 1 - Standard chests
; 3- Gold
@GetChestColor:
    cmp r0, 0x160 ; Expanded item IDs
    bgt @@CheckExpandedItemColors
    cmp r0, 0x76 ; All relics and Glyphs should use gold chests.
    movlt r0, 0x03
    blt @@End
    cmp r0, 0xE5 ; All Equipment should use standard chests.
    movgt r0, 0x01
    bgt @@End
    cmp r0, 0xD6 ; AP Prog items
    moveq r0, 0x03
    beq @@End
    cmp r0, 0xD5 ; AP Useful items
    moveq r0, 0x01
    beq @@End
    cmp r0, 0xD4 ; AP Filler
    moveq r0, 0xFF
    beq @@End
    mov r0, 0x01 ; All consumables end up with Standard chests. Change in future?
@@End:
    cmp r0, 0xFF
    addeq r0, r0, 0xFF00 ; Set the high bit to make it -1
    bx lr
@@CheckExpandedItemColors:
    sub r0, r0, 1
    sub r0, r0, 0x160
    cmp r0, 0x07 ; Money uses brown chests
    movle r0, 0xFF
    ble @@End
    mov r0, 0x03 ; Villagers and maps always use gold chests
    b @@End

; Tells normal chests to draw as wooden chests based on their color.
@RamFlag_ChestIsBlue:
    .db 0x00
.align 4

@GetChestSprite:
    push lr
    ldr r0, =@RamFlag_ChestIsBlue
    ldrb r0, [r0]
    cmp r0, 0
    movne r0, 4 ; Force to normal chesy
    bne @@End
    ldrh r0, [r4, 0x66]
    bl @GetChestColor
    cmp r0, 0xFF ; If it's a wood chest
    movge r0, 0 ; Wood chest
    movlt r0, 4 ; Normal chests
@@End:
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;
; Handles text popups for extended glyphs
@WriteExtendedGlyphName:
    push r0
    ldr r0, [r5, 0xD8]
    cmp r0, 0x70
    blt @@NormalGlyph
    bl @GetTextIDFromItem
    mov r2, r0
    pop r0
    bl 0x0209D0D0 ; Show the main popup
    ldr r1, [r5, 0x0D8]
    cmp r1, 0x160
    bgt @@GetExpandedText
    cmp r1, 0xD6
    moveq r1, 0x54 ;ap prog
    beq @@End
    cmp r1, 0xD5
    moveq r1, 0x55 ; ap use
    beq @@End
    cmp r1, 0xD4
    moveq r1, 0x56 ; ap filler
    beq @@End
    mov r1, 0x57 ; Normal items
    b @@End
@@GetExpandedText:
    sub r1, r1, 1
    sub r1, r1, 0x160
    cmp r1, 0x07
    movlt r1, 0x58 ; money
    blt @@End
    cmp r1, 0x15
    bge @@MapText
    mov r1, 0x59 ; Villagers
    b @@End
@@MapText:
    mov r1, 0x53 ; Maps
@@End:
    mov r3, r1
    bl 0x0209D130
    b 0x0206DA08
@@NormalGlyph:
    pop r0
    bl 0x0209D0D0
    b 0x0206D9F0

;Gets an item text ID from an item, including Expandeds.
@GetTextIDFromItem:
    cmp r0, 0x160
    bgt @@GetExpanded
    add r0, r0, 0x15
    bx lr
@@GetExpanded:
    sub r0, r0, 1
    sub r0, r0, 0x160
    cmp r0, 0x07
    blt @@MoneyText
    cmp r0, 0x15
    blt @@VillagerText
    sub r0, r0, 0x15
    add r0, r0, 0x5A0
    add r0, r0, 1
    bx lr
@@MoneyText:
    add r0, r0, 0x3CC
    bx lr
@@VillagerText:
    sub r0, r0, 0x07
    add r0, r0, 0x03
    bx lr
;;;;;;;;;;;;;;;;;;;;;
; Names for the non-standard Glyphs used on events
@SpecialGlyphNames:
    @MapGlyph:
        .db 0x01, 0x00, 0x34, 0x41, 0x42, 0x55, 0x4C, 0x41, 0x00, 0x32, 0x45, 0x47, 0x49, 0x4F, 0x4E, 0x49, 0x53, 0xEA
    @ProgGlyph:
        .db 0x01, 0x00, 0x32, 0x45, 0x53, 0x00, 0x30, 0x52, 0x4F, 0x47, 0x52, 0x45, 0x53, 0x53, 0x49, 0x4F, 0x4E, 0x49
        .db 0x53, 0xEA
    @UsefulGlyph:
        .db 0x01, 0x00, 0x32, 0x45, 0x53, 0x00, 0x35, 0x54, 0x49, 0x4C, 0x49, 0x53, 0xEA
    @FillerGlyph:
        .db 0x01, 0x00, 0x32, 0x45, 0x53, 0x00, 0x23, 0x4F, 0x4D, 0x50, 0x4C, 0x45, 0x54, 0x4F, 0x52, 0x49, 0x41, 0xEA
    @ItemGlyph:
        .db 0x01, 0x00, 0x34, 0x48, 0x45, 0x53, 0x41, 0x55, 0x52, 0x55, 0x53, 0xEA
    @MoneyGlyph:
        .db 0x01, 0x00, 0x30, 0x45, 0x43, 0x55, 0x4E, 0x49, 0x41, 0xEA
    @VillagerGlyph:
        .db 0x01, 0x00, 0x36, 0x49, 0x43, 0x41, 0x4E, 0x55, 0x53, 0xEA
.align 4
;;;;;;;;;;;;;;;;;;;;;;;;;;
; Handle a variable that this is a Blue chest so it skips the sprite func
@MakeBlueChest:
    push lr
    push r0, r1
    ldr r0, = @RamFlag_ChestIsBlue
    mov r1, 1
    strb r1, [r0]
    pop r0, r1
    bl 0x0221A408
    push r0, r1
    ldr r0, = @RamFlag_ChestIsBlue
    mov r1, 0
    strb r1, [r0]
    pop r0, r1
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;
; Sets all flags for starting villagers
@GetStartingVillagers:
    push r1,lr
    ldr r0, =@OptionFlag_StartingVillagers
    ldrh r0, [r0]
    mov r2, 0
    mov r3, 1
@@VillagerLoop:
    lsl r1, r3, r2 ; Shift to get the current bit ID
    tst r0, r1
    beq @@VillagerNotSet
    push r0
    mov r0, r2 ; Villager index
    bl @UnlockVillager
    pop r0
@@VillagerNotSet:
    add r2, r2, 1
    cmp r2, 0x0D
    bne @@VillagerLoop
    pop r1,lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;;
; Auto reveals breakables if necessary
@CheckBreakableWalls:
    push r0
    ldr r0, =@OptionFlag_RevealHiddenWalls
    ldrb r0, [r0]
    cmp r0, 0
    pop r0
    beq @@NormalCheck
    mov r0, 1
    bx lr
@@NormalCheck:
    ldrsh r0, [r0, 0x72]
    bx lr
;;;;;;;;;;;;;;;;;;;;;
; Reveals the map if necessary
@AutoMapReveal:
    push r0
    ldr r0, =@OptionFlag_RevealMap
    ldrb r0, [r0]
    cmp r0, 0
    pop r0
    beq @@NormalMap
    mov r2, 1
@@NormalMap:
    cmp r2, 1
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;
;  Grabs object's varA in r3. Used for hardcoded blue chests.
@SetStaticChest:
    add r3, r4, 0x100
    ldrh r3, [r3, 0x3C] ; varA
    bx lr

; For Cubus in monastery
@SetStaticChest_cubes:
    add r3, r8, 0x100
    ldrh r3, [r3, 0x3C] ; varA
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;
; if VarA >= 0x8000, act like VarA is 0
@SetExtendedGlyphStatues:
    ldrh r2, [r1, 0x3C]
    cmp r2, 0x8000
    blt @@SkipRemove
    mov r2, 0  ; We want to treat anything above 0x8000 as if it were 0 so it acts like a statue
@@SkipRemove:
    bx lr

@CheckExtendedStatueAsGlyph:
    ldrh r3, [r2, 0x3C]
    cmp r3, 0x8000
    blt @@SkipRemove
    mov r3, 0  ; We want to treat anything above 0x8000 as if it were 0 so it acts like a statue
@@SkipRemove:
    bx lr

@CheckExtendedStatueAsGlyphParticle:
    ldrh r3, [r0, 0x3C]
    cmp r3, 0x8000
    blt @@SkipRemove
    mov r3, 0  ; We want to treat anything above 0x8000 as if it were 0 so it acts like a statue
@@SkipRemove:
    bx lr

; Normally, Glyph Statues use VarB (Glyph ID) + 1 as their flag. Instead, we want to use VarA
; Glyph Statues will set bit 0x8000 to know it's a statue, and use the rest of VarA as the flag.
@GetGlyphStatueFlag:
    ldrh r2, [r1, 0x3C]  ; This code only runs for statues, so it's okay to use VarA (candle type)
    mov r1, 0x8000
    sub r1, r1, 1
    ands r2, r2, r1 ; Unset the High flag
    bx lr

; Similar to the above, but when spawning the Glyph so it knows which flag to set.
@SetGlyphStatueFlag:
    ldrh r0, [r2, 0x3C]
    mov r1, 0x8000
    sub r1, r1, 1
    ands r0, r0, r1
    bx lr
;;;;;;;;;;;;;;;;;;;
; If creating a Wall pickup that's a villager, create that Villager instead
@SpawnVillagerInWall:
    push lr
    add r1, r0, 0x100
    ldrh r1, [r1, 0x3E] ; Check the Item ID
    cmp r1, 0x168
    blt @@SpawnItem
    sub r1, r1, 0x168
    cmp r1, 0x0D
    bge @@SpawnItem
@@SpawnVillager:
    add r1, r0, 0x100
    ldrh r1, [r1, 0x3E] ; Get the Item ID
    sub r1, r1, 0x168 ; Get villager Index
    mov r0, r1
    bl 0x022349F8
    ldrb r0, [r0, 0x08] ; Get the villager's ID number
    mov r1, r0
    add r0, r4, 0x100
    ldrh r2, [r0, 0x3C] ; Get the original VarA
    strh r1, [r0, 0x3C] ; Set the Villager ID as VarA
    strh r2, [r0, 0x3E] ; Set the original VarA as the VarB event flag
    sub r0, r0, 0x100
    bl 0x0223183C
    ldr r2, =0x02231ABC
    str r2, [r4]
    pop lr
    mov r0, 0
    bx lr
@@SpawnItem:
    ; Normal spawn func
    bl 0x0206427C
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;;;
; If we already checked the Flag for this glyph, don't give it again.
; This is to prevent Progressives from proccing twice
@RamFlag_GlyphUnlocked:
.db 0x00
.align 4
@SkipExcessGlyphItems:
    push lr
    cmp r0, 0x168  ; We only care about our Progressive items here
    blt @@SkipExtendedCheck
@@CheckForMax:
    ldr r0, =@RamFlag_GlyphUnlocked
    ldrb r1, [r0]
    cmp r1, 0
    bne @@SkipItem
    ldr r0, [r5, 0xD8]
    b @@GiveItem
@@SkipExtendedCheck:
    cmp r0, 0x80 ; max ups
    blt @@GiveItem
    cmp r0, 0x82
    bgt @@GiveItem
    b @@CheckForMax
@@GiveItem:
    cmp r0, 0x80
    blt @@Normal
    cmp r0, 0x82
    bgt @@Normal
    bl 0x02063EAC
    b @@SkipItem

@@Normal:
    bl 0x020635A4
@@SkipItem:
    ldr r0, =@RamFlag_GlyphUnlocked
    mov r1, 0
    strb r1, [r0]
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;
; Checks for a flag to be set for the Albus events
@RAMFlag_AlbusGlyphFlag:
.dh 0x0000
.align 4
@SetEventGlyphFlag:
    push r5
    ldr r0, =@RAMFlag_AlbusGlyphFlag
    ldrb r0, [r0]
    cmp r0, 0
    beq @@SetFlagNormal
    mov r1, r0
    ldr r0, =@RAMFlag_AlbusGlyphFlag
    mov r5, 0
    strb r5, [r0]
    pop r5
    b 0x02230030
@@SetFlagNormal:
    add r1, r1, 1
    pop r5
    b 0x02230030

; Loads the flag for the Albus 1 Event.
@SetMineraAlbusGlyph:
    ldr r1, = @RAMFlag_AlbusGlyphFlag
    mov r0, 0x33
    strb r0, [r1]
    mov r0, r4
    bx lr

; Loads the flag for the Albus 2 Event.
@SetDwellingAlbusGlyph:
    ldr r1, = @RAMFlag_AlbusGlyphFlag
    mov r0, 0x34
    strb r0, [r1]
    mov r0, r4
    bx lr

@SetManorAlbusGlyph:
    push r0,r1
    ldr r1, = @RAMFlag_AlbusGlyphFlag
    mov r0, 0x35
    strb r0, [r1]
    pop r0,r1
    bx lr
;;;;;;;;;;;;;;;
; Delay the fade when leaving an area so we can see what we got
@DelayAreaFade:
    push r0-r3
    ldr r0, = @RamFlag_AreaExitDelay
    ldrh r1, [r0]
    cmp r1, 0 ; If this isn't set, we don't want to delay at all.
    beq @@Exit
    ldr r2, = 0x020FFC8C ; State flags
    ldrb r3, [r2, 0x02]
    orr r3, r3, 0x10 ; Set the RoomTransition flag so the player can't move
    strb r3, [r2, 0x02]
    sub r1, r1, 1
    cmp r1, 0 ; If we JUST hit 0
    beq @@ResetAndExit
    strb r1, [r0]
    pop r0-r3
    b 0x0221D8BC  ; Exit without updating State so we don't proceed

@@ResetAndExit:
    ldrb r3, [r2, 0x02]
    and r3, r3, 0xEF ; Reset the flag we just set
    strb r3, [r2, 0x02]
    strb r1, [r0] ; and reset the delay counter
@@Exit:
    pop r0-r3
    bl 0x02027258
    b 0x0221D6F8

; Normally the flag for being busy skips this part, but we want to check it so our fade logic can run
@CheckAreaDelay:
    tst r0, 0x40
    bne @@ResetOnDeath
    push r0
    ldr r0, =@RamFlag_AreaExitDelay
    ldrh r0, [r0]
    cmp r0, 0
    pop r0
    beq @@TestNormal
    mov r5, 1 ; Ignore this check so we can run fade logic
    b 0x0221D6BC
@@TestNormal:
    tst r0, 0x41
    b 0x0221D6B8

; I'm not sure we need the reset, but failsafe in case it happens
@@ResetOnDeath:
    push r0,r1
    ldr r0, =@RamFlag_AreaExitDelay
    mov r1, 0
    strh r1, [r0] ; Clear so it doesn't go through on a reload
    pop r0,r1
    mov r5, 0
    b 0x0221D6BC


.pool
.endarea
.close


; Money is items 0x161-167
; Villagers are 168-175
; Map ids are 176 and above