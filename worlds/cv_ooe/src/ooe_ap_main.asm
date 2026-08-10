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
        ;bl @SwapGlyphFile4

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

    .org 0x02065348
        b @GetBossPortalPosition

    .org 0x02061F48
        bl @GetBossChestItems

    .org 0x020378F4
        bl @OneScreen_OpenMap

    .org 0x02037388
        b @ExitDebugMap

    .org 0x0203735C
        bl @DebugMap_DrawMarker

    .org 0x020425EC
        bl @DebugMap_DrawX

    .org 0x02042620
        bl @DebugMap_DrawY

    .org 0x02045D08
        b @DebugMap_Close

    .org 0x02045C10
        b @DebugMap_SkipWarpLogic

    .org 0x020379B0
        bl @OneScreen_DisableScreenSwap

    .org 0x02045A74
        b @DebugMap_SkipLogic2

    .org 0x020379B4
        bl @OneScreen_DontResetTopType

    .org 0x02088174
        bl @CheckIfEnemGlyphObtained  ; Used for the Top Screen enemy status

    .org 0x0204D0CC
        bl @CreateAndClearDeaths

    .org 0x020378FC
        bl @RemoteKillPlayer

    .org 0x0200BED0
        bl @SwapLoadedGlyphPointer


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
        .dw @RelicGlyph

    .org 0x021FCA1C
        .dw @CatHint1

    .org 0x021FCA24
        .dw @CatHint2

    .org 0x021FCA2C
        .dw @CatHint3

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

    .org 0x0220576C
        mov r2, 0x04  ; Bone Archer glyph flag

    .org 0x02213944
        mov r0, 0x2E ; Nova Skeleton glyh

    .org 0x0221312C
        mov r0, 0x30 ; Hammer Shaker glyph

    .org 0x02223BF0
        .dh 0x075B ; Cat 1 second text ID

    .org 0x02223BF4
        .dh 0x0757 ; Cat 2 second text ID

    .org 0x02223BF8
        .dh 0x0759 ; Cat 3 second text ID
.close
;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_20", 0x021FFFC0
    .org 0x02213F48
        b 0x02214090 ; Skip opening logos

    .org 0x02214340
        cmp r0, 1 ; Make the first opening movie fade faster

    .org 0x022143B8
        cmp r0, 0xFF ; Make the first opening switch to the title faster

    .org 0x02205F30
        mov r0, 1 ; Hard mode

    .org 0x02206604
        beq 0x022064F0 ; Fix being unable to back out of difficulty selection
        
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
        b 0x02237714  ; Don't give Barlowe's Albus 1 dialogue priority over the Dominus handler

    .org 0x022A194C
        bl @TinManChestItem

    .org 0x0227934C
        bl @SpawnPortal_GiantSkeleton

    .org 0x02295E28
        bl @PortalSpawn_ModeCheck

    .org 0x022B6AA6  ; Boss rush portal position for Giant Skeleton on Minera.
        .db 0x08, 0x00
        .dh 0x20, 0xA0

    .org 0x022B6B3E ; Some sort of order used for portals. Not sure why they dont just use varA....
        .db 0x02 ; Set this to Giant Skeleton instead of 0

    .org 0x022B6B46 ; Some sort of order used for portals. Not sure why they dont just use varA....
        .db 0x0A ; Set this to Wallman instead 0f 0

    .org 0x02296120
        bl @ResetBossFlagOnPortal

    .org 0x02295F74
        bl @SetPortalIndex

    .org 0x02296160
        bl @TeleportOutOfBrach

    .org 0x022B6AE8
        .dh 0x02C0 ; Gravedorcus's Portal Position

    .org 0x022B6B1A
        .dh 0x50 ; Eligor's Portal Position

    .org 0x02295F88
        bl @DontExitGame

    .org 0x02237720
        b 0x0223774C ; Barlowe's dialogue after Albus 2. Skip this and defer to the generic handler

    .org 0x02296B0C
        b @LockBossDoor

    .org 0x022792CC
        bl @SkeletonFlightDisable

    .org 0x0223967C
        bl @PostBarloweWarp

    .org 0x02231B74
        b 0x02231B88 ; The check for Anna's cat. This just crashes if we're out of the room...

    .org 0x02231EF4
        b 0x02231F04 ; The same, for when we're deleting the object

    .org 0x02230048
        bl @ClampVillagerGlyphPos

    .org 0x02293074
        mov r3, 0x01 ; Bone Scimitar glyph flag

    .org 0x022629EC
        mov r0, 0x02 ; Axe knight glyph flag

    .org 0x0224E8B4
        b @SetNecromancerGlyph

    .org 0x0222B09C
        bl @CheckIfEnemGlyphObtained  ; Used for the Guide menu

    .org 0x0222D260
        bl @CheckIfEnemGlyphObtained_BestMain ; Used on the Bestiary's top menu

    .org 0x0227508C
        bl @SetSpearGuardGlyph

    .org 0x0228A464
        mov r0, 0x09 ; Skull Spider g flag

    .org 0x0225C860
        mov r0, 0x0E ; Sea Demon g flag

    .org 0x0225AB24
        mov r0, 0x0F ; Fire Demon g flag

    .org 0x022524E4
        bl @SetWerebatGlyphFlag

    .org 0x0223E654
        bl @SetDullahanGlyphFlag

    .org 0x02249250
        bl @SetMissMurderGlyphFlag

    .org 0x0226E838
        bl @SetLizardmanGlyphFlag

    .org 0x02258F08
        mov r0, 0x23 ; Thunder Demon glyph flag

    .org 0x022502CC
        bl @SpawnFomorGlyph

    .org 0x0228AE54
        bl @SetPantherGlyphFlag

    .org 0x02276CBC
        bl @SetPolkirGlyphFlag

    .org 0x0224C05C
        mov r1, 0x2F ; Red Smasher glyph

    .org 0x0228CBD8
        bl @SetAutomatonGlyphFlag

    .org 0x02261A64
        mov r0, 0x38 ; Gorgon Head glyph

    .org 0x022520A4
        bl @SetGreatKnightGlyphFlag

    .org 0x02262338
        mov r0, 0x3B ; Winged Skeleton Glyph

    .org 0x0225E73C
        mov r0, 0x5E

        
.close
;;;;;;;;;;;;;;;;;;;;;;

.open "ftc/overlay9_24", 0x022B73A0
    .org 0x022BA1EC
        bl @SpawnPortal_Arthro
.close
;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_25", 0x022B73A0
    .org 0x022BC2FC
        bl @SpawnPortal_Death
.close
;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_26", 0x022B73A0
    .org 0x022BAD68
        bl @SpawnPortal_Maneater
.close
;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_27", 0x022B73A0
    .org 0x022BB64C
        bl @SpawnPortal_Rasulka
.close
;;;;;;;;;;;;;;;;;;;;;

.open "ftc/overlay9_28", 0x022B73A0
    .org 0x022B9690
        mov r0, 6  ; Wallman's Glyph flag

    .org 0x022BA518
        bl @SpawnPortal_Wallman

.close
;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_29", 0x022B73A0
    .org 0x022B94F8
        mov r0, 0x58 ; Jiang Shi glyph flag
.close
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_30", 0x022B73A0
    .org 0x022B97BC
        bl @SpawnPortal_Brach

    .org 0x022B97CC
        nop ; Second blue chest at 0, 0?????

.close
;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_31", 0x022B73A0
    .org 0x022BD908
        bl @SpawnPortal_Eligor
.close
;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_32", 0x022B73A0
    .org 0x022BC164
        bl @SpawnPortal_Goliath

.close
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_33", 0x022B73A0
    .org 0x022BA0D0
        bl @SpawnPortal_Dorcus

.close
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_35", 0x022B73A0
    .org 0x022B9A60
        bl @SpawnPortal_Blackmore
.close
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_36", 0x022B73A0
    .org 0x022B9068
        bl @SpawnPortal_Albus

    .org 0x022B906C
        bl @SpawnAlbusMissedGlyph

    .org 0x022B8DB0
        b @DontRespawnAlbusGlyph

    .org 0x022B8338
        mov r0, 0x63 ; Albus Glyph Flag

.close
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_37", 0x022B73A0
    .org 0x022B73DC
        bl @SpawnPortal_Barlowe

    .org 0x022B73E0
        bl @SpawnBarloweMissedGlyph

    .org 0x022B8150
        bl @HandlePostBarloweFight

    .org 0x022BA998
        mov r0, 0x7C ; Barlowe glyph flag
.close
;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_38", 0x022B73A0
    .org 0x022BE308
        bl @SetSpecSwordGlyphFlag

    .org 0x022B9E58
        mov r0, 0x25 ; Owl glyph flag
.close
;;;;;;;;;;;;;;;;;;;;;
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
;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_68", 0x022C1FE0
    .org 0x022C2CB0
        bl @SetStaticGlyph ; Labyrinth boulder room
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
        .db 0x00 ; Unused
    @OptionFlag_EXPMult:
        .dh 0x00 ; 022EB230
    @RomVar_TinManItem:
        .dh 0x00 ; 022EB232
.align 4
    @OptionFlag_MedalChests: ; 022Eb234
        .db 0x00
    @OptionFlag_BarloweRequired: ;022Eb235
        .db 0x00
    @OptionFlag_APMult: ;022EB236
        .db 0x01
    @OptionFlag_OneScreenMode: ; 022EB237
        .db 0x00
    @OptionFlag_OpenCastle: ;022EB238
        .db 0x00
.align 0x10
    @ROMTable_BossChestItems: ;022EB240
        .dh 0xD8
        .dh 0xD9
        .dh 0xDA
        .dh 0xDB
        .dh 0xDC
        .dh 0xDD
        .dh 0xDE
        .dh 0xDF
        .dh 0xE0
        .dh 0xE1
        .dh 0xE2
        .dh 0xE3
        .dh 0xE4
    @ROMTable_EnemyGlyphIndex:  ; Indexed list of enemies which have Glyphs attached to them
        .db 0x05
        .db 0x08
        .db 0x0B
        .db 0x0C
        .db 0x0D
        .db 0x18
        .db 0x1A
        .db 0x1E
        .db 0x22
        .db 0x23
        .db 0x28
        .db 0x33
        .db 0x38
        .db 0x3B
        .db 0x3C
        .db 0x45
        .db 0x4C
        .db 0x50
        .db 0x51
        .db 0x55
        .db 0x5A
        .db 0x5E
        .db 0x5F
        .db 0x61
        .db 0x63
        .db 0x65
        .db 0x67
        .db 0x68
        .db 0x72
        .db 0x73
        .db 0x74
.align 4
    @ROMTable_EnemyGlyphFlags:  ; Index of which flag each enemy uses for its Glyph.
        .dh 0x01 ; Bone Scimitar
        .dh 0x02 ; Axe Knight
        .dh 0x03 ; Necromancer
        .dh 0x04 ; Bone Archer
        .dh 0x08 ; Spear Guard
        .dh 0x09 ; Skull Spider
        .dh 0x0E ; Sea Demon
        .dh 0x0F ; Fire Demon
        .dh 0x12 ; Werebat
        .dh 0x14 ; Black Formor
        .dh 0x16 ; Dullahan
        .dh 0x19 ; Miss Murder
        .dh 0x1C ; Lizardman
        .dh 0x23 ; Thunder Demon
        .dh 0x25 ; Owl
        .dh 0x27 ; White Formor
        .dh 0x2A ; Black Panther
        .dh 0x2B ; Polkir
        .dh 0x2E ; Nova Skeleton
        .dh 0x2F ; Red Smasher
        .dh 0x30 ; Hammer Shaker
        .dh 0x36 ; Spectral Sword
        .dh 0x37 ; Automaton ZX27
        .dh 0x38 ; Gorgon Head
        .dh 0x39 ; Great Knight
        .dh 0x3B ; Winged Skeleton
        .dh 0x58 ; Jiang Shi
        .dh 0x5E ; Demon Lord
        .dh 0x63 ; Albus
        .dh 0x7C ; Barlowe
        .dh 0x06 ; Wallman
    @EnemGlyphIndex_len equ @ROMTable_EnemyGlyphFlags - @ROMTable_EnemyGlyphIndex
.align 4
    @OptionFlag_StolenGlyphChecks:
        .db 0x01 ; 022EB2BC
    @OptionFlag_GlyphDropMult:
        .db 0x00 ; 022EB2BD
    @OptionFlag_DeathLinkEnabled:
        .db 0x00 ; 022EB2BE
    @RAMFlag_ReceivedServerDeath:
        .db 0x00 ; 022EB2BF

.align 0x10
    @CatHint1: ;022EB2C0
        .fill 0xB0
    @CatHint2:
        .fill 0xB0 ;22EB370
    @CatHint3:
        .fill 0xB0 ; 22EB420

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
    mov r1, 1
    mov r2, 1
    ldr r0, = @OptionFlag_OneScreenMode
    ldrb r0, [r0]
    cmp r0, 0
    moveq r0, 5
    movne r0, 7
    push r1
    ldr r1, = 0x0210078D
    strb r0, [r1]
    pop r1
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
    bl @GetGlyphAP
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
    ldr r0, = @OptionFlag_OpenCastle
    ldrb r0, [r0]
    cmp r0, 0
    beq @@SkipCastleUnlock
    mov r0, 0
    mov r1, 1
    bl 0x020AA95C ; Set Dracula's Castle as unlocked

@@SkipCastleUnlock:
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
    ldreq r0, =0x343 ; AP prog 
    bxeq lr
    cmp r0, 0xD4
    ldreq r0, =0x342
    bxeq lr
    cmp r0, 0xD5 ; AP Useful
    ldreq r0, =0x346
    bxeq lr


    cmp r0, 0x160
    bgt @@ExpandedItems
    cmp r0, 0x75
    ldrle r0, =0x347 ; Relics 
    bxle lr

    ldr r0, = 0x341 ; Regular items
    bx lr
    ; Custom items here
@@ExpandedItems:
    sub r0, r0, 1
    sub r0, r0, 0x160
    cmp r0, 0x07
    ldrlt r0, =0x344 ; Money glyphs
    bxlt lr
    cmp r0, 0x15
    ldrge r0, =0x345 ; Maps
    bxge lr
    ldr r0, =0x340; villagers
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
    strh r2, [r1, 0x3E] ; 0 out VarB so it doesn't read as a loc flag
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
    movlt r0, 0xFF
    blt @@End
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
.pool
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
    cmp r1, 0x75
    movle r1, 0x5A ; Relics
    ble @@End


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
    add r0, r0, 0x430
    add r0, r0, 0x0D
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
    @RelicGlyph:
        .db 0x01, 0x00, 0x32, 0x45, 0x4C, 0x49, 0x51, 0x55, 0x49, 0x41, 0xEA
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
    mov r0, 0x1F
    push r0-r2
    bl 0x020635A4 ; get a free Torpor for every starting Villager
    pop r0-r2

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
;;;;;;;;;;;;;;;;;;;;
; Load into r3 the item on the Tin Man chest in Minera
@TinManChestItem:
    ldr r3, = @RomVar_TinManItem
    ldrh r3, [r3]
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Spawn Arthroverta's Boss Portal
@SpawnPortal_Arthro:
    push lr
    bl 0x02061F0C
    mov r0, 1 ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop lr
    bx lr

; Spawn Giant Skeleton's Boss Portal
@SpawnPortal_GiantSkeleton:
    push lr
    bl 0x02061F0C
    mov r0, 2 ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop lr
    bx lr


; Spawn Brachyura's boss portal
@SpawnPortal_Brach:
    push r5, lr
    bl 0x02061F0C
    ldr r0, = 0x021003E4
    ldr r0, [r0]
    tst r0, 0x08
    beq @@SpawnBrachPreBossPortal
    mov r0, 3 ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
@@IsSafe:
    pop r5, lr
    bx lr
@@SpawnBrachPreBossPortal:
    ; If the player lacks any movement, we want to spawn a portal to warp out of here
    mov r0, 0x71
    bl 0x020633F0 ; Check if we own Double Jump
    cmp r0, 0
    bne @@IsSafe ; If we're not softlocked, we dont need to spawn a backup portal
    mov r0, 0x3B
    bl 0x020633F0 ; Flight
    cmp r0, 0
    bne @@IsSafe
    mov r0, 0x39 ; Magnes
    bl 0x020633F0
    cmp r0, 0
    bne @@IsSafe
    mov r2, 0xFF ; Use this as a special indicator for the portal
    bl @SpawnBossPortal
    b @@IsSafe

; Spawn Man Eater's Boss Portal
@SpawnPortal_Maneater:
    push r5, lr
    bl 0x02061F0C
    mov r0, 4 ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop r5, lr
    bx lr

; Spawn Rasulka's portal
@SpawnPortal_Rasulka:
    push r5, lr
    bl 0x02061F0C
    mov r0, 5 ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop r5, lr
    bx lr

@SpawnPortal_Goliath:
    push r5, lr
    bl 0x02061F0C
    mov r0, 6 ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop r5, lr
    bx lr

@SpawnPortal_Dorcus:
    push r5, lr
    bl 0x02061F0C
    mov r0, 7 ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop r5, lr
    bx lr

;NOTE!!!!
;If I do Glyphsanity I'll need to respawn this portal even if the boss is dead if we don't have the check.
@SpawnPortal_Albus:
    push r5, lr
    bl 0x02061F0C
    mov r0, 8 ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop r5, lr
    bx lr

;NOTE!! If I do Glyphsanity I'll need to respawn this portal too
@SpawnPortal_Barlowe:
    push r5, lr
    bl 0x02061F0C
    mov r0, 9 ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop r5, lr
    bx lr

@SpawnPortal_Wallman:
    push r5, lr
    bl 0x02061F0C
    mov r0, 0x0A ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop r5, lr
    bx lr

@SpawnPortal_Blackmore:
    push r5, lr
    bl 0x02061F0C
    mov r0, 0x0B ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop r5, lr
    bx lr

@SpawnPortal_Eligor:
    push r5, lr
    bl 0x02061F0C
    mov r0, 0x0C ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop r5, lr
    bx lr

@SpawnPortal_Death:
    push r5, lr
    bl 0x02061F0C
    mov r0, 0x0D ; Boss death flag
    mov r5, r6
    bl @RespawnBoss
    pop r5, lr
    bx lr




; If we miss a Medal chest, we need to respawn it. Do that here.
@RespawnBoss:
    push lr
    ldr r1, = @OptionFlag_MedalChests
    ldrb r1, [r1]
    cmp r1, 0 ; If the Medal Chest option is disabled, just bail out
    beq @@Exit
    ldr r2, = 0x021003E4
    ldr r2, [r2]
    mov r1, 1
    lsl r1, r1, r0
    tst r1, r2
    beq @@Exit


    mov r2, r0
    sub r0, r0, 1
    add r0, r0, 0x160 ; Loc flags for beating the boss with no damage
    bl @CheckLocFlag
    cmp r0, 0
    bne @@Exit ; If we have already gotten this boss with no damage, don't spawn a portal
    mov r0, r2
    bl @SpawnBossPortal
@@Exit:
    pop lr
    bx lr

; Spawns a portal for r0 boss.
@RamFlag_PortalSpawn:
.db 0x00
.align 4

@SpawnBossPortal:
    push lr
    ldr r0, = @RamFlag_PortalSpawn
    strb r2, [r0]
    mov r0, 2
    mov r1, 0x11
    bl 0x0206520C ; Creat the portal object
    ldr r0, = @RamFlag_PortalSpawn
    mov r1, 0
    strb r1, [r0]
    pop lr
    bx lr

; Boss portals normally bail if you're not in Boss Rush mode.
; if we're creating one, don't check this.
@PortalSpawn_ModeCheck:
    ldr r3, =@RamFlag_PortalSpawn
    ldrb r3, [r3]
    cmp r3, 0
    beq @@Exit
    mov r3, 1
    cmp r3, 1 ; Force the cmp when we get back to fail
    bx lr
@@Exit:
    cmp r1, 2
    bx lr

; Sets up the Position variables for our boss portals
@GetBossPortalPosition:
    push r0
    ldr r0, = @RamFlag_PortalSpawn
    ldrb r0, [r0]
    cmp r0, 0
    beq @@Exit
    cmp r0, 3 ; Brachyura
    popeq r0
    beq @@LighthousePortalCoord
    cmp r0, 0xFF ; Speical lighthouse exit
    popeq r0
    beq @@SpawnLighthouseNormalPortal
    cmp r0, 0x07
    popeq r0
    beq @@PortalPos_Dorcus
    cmp r0, 0x0A
    popeq r0
    beq @@PortalPos_Wallman
    cmp r0, 0x0B
    popeq r0
    beq @@PortalPos_Black
    cmp r0, 0x0C
    popeq r0
    beq @@PortalPos_Eligor


    pop r0

    push r1
    push r0
    ldr r0, = 0x0213A5C0
    ldrh r0, [r0, 0x38] ; Get the room width
    mov r1, 2
    bl 0x02023E68 ; Divide width  by 2
    mov r1, 0x10
    bl 0x02023E68 ; Divide THAT by 10

    mov r1, r0
    pop r0
    strh r1, [r0, 0x32] ; Center the portal horizontally
    mov r1, 0x0B
    strh r1, [r0, 0x36] ; Need this for it to be visible
@@ExitLighthouseSpawn:
    ldr r1, = @RamFlag_PortalSpawn
    ldrh r1, [r1]
    ;sub r1, r1, 1 ; Use this for Boss Index

    add r0, r0, 0x100
    strh r1, [r0, 0x3C]
    sub r0, r0, 0x100


    pop r1
    blx r1 ; Spawn the object
    b 0x02065354  ; Normally this function deletes the object after spawning it. We don't want to do that, so skip the delete code
@@Exit:
    pop r0
    blx r1
    b 0x0206534C
@@LighthousePortalCoord:
    push r1
    mov r1, 0x02 ; Spawn the portal in the door frame
    strh r1, [r0, 0x32]
    mov r1, 0xA4
    strh r1, [r0, 0x36]
    b @@ExitLighthouseSpawn
    pop r1
@@SpawnLighthouseNormalPortal:
    push r1
    mov r1, 0x03
    strb r1, [r0, 0x0D] ; Set it to auto warp
    b @@ExitLighthouseSpawn
    pop r1
@@PortalPos_Dorcus:
    push r1
    mov r1, 0x09 ; Dorcus has a special floor that's raised up too high for the portal
    strb r1, [r0, 0x36]
    mov r1, 0x18
    strh r1, [r0, 0x32]
    b @@ExitLighthouseSpawn
    pop r1
@@PortalPos_Wallman:
    push r1
    mov r1, 0x0B
    strb r1, [r0, 0x36]
    mov r1, 0x07
    strh r1, [r0, 0x32] ; Wallman's room is split in half, spawn the portal on the left side
    b @@ExitLighthouseSpawn
    pop r1
@@PortalPos_Black:
    push r1
    mov r1, 0x0A
    strb r1, [r0, 0x36]
    mov r1, 0x10
    strh r1, [r0, 0x32] ; Blackmore ALSO has a raised up floor
    b @@ExitLighthouseSpawn
    pop r1
@@PortalPos_Eligor:
    push r1
    mov r1, 0x17
    strb r1, [r0, 0x36]
    mov r1, 0x04
    strh r1, [r0, 0x32] ; Blackmore ALSO has a raised up floor
    b @@ExitLighthouseSpawn

; We just entered a Boss Portal, so we want to reset its flag.
@ResetBossFlagOnPortal:
    ldr r0, = 0x02100790
    ldrb r1, [r0]
    cmp r1, 2 ; If we're using this portal in Boss Rush, just handle it like normal.
    beq @@Exit
    add r0, r4, 0x100
    ldrh r0, [r0, 0x3C] ; grab the var A
    cmp r0, 3
    beq @@ResetLighthouse
@@lightreset:
    mov r1, 1
    lsl r0, r1, r0 ; SHift boss id into bit
    ldr r1, =0x021003E4
    ldr r2, [r1]
    bic r2, r2, r0 ; We want to Unset the boss death flag here
    str r2, [r1]
@@Exit:
    mov r0, 0
    bx lr
@@ResetLighthouse:
    ; Lighthouse needs to also reset the elevator flag
    push r0
    ldr r1, =0x02100378
    ldrb r0, [r1]
    bic r0, r0, 0x01
    strb r0, [r1]
    pop r0
    b @@lightreset

; Most bosses index their flag to find the next boss. So we sub 1 here.
@SetPortalIndex:

    ldrh r2, [r0, 0x3C]
    ldr r1, =0x02100790
    ldrb r1, [r1]
    cmp r1, 2 ; boss rosh
    beq @@Skip

    cmp r2, 2 ; Skeleton
    beq @@Skip
    cmp r2, 0x0A
    beq @@Skip ; Drac bosses
    cmp r2, 0x0B
    subeq r2, r2, 1 ; Sub an extra for Blackmore


    cmp r2, 3 ; Brach
    moveq r2, 2
    sub r2, r2, 1
@@Skip:
    bx lr

; Warp out of Brachyura's room so we dont softlock
@TeleportOutOfBrach:
    push r0
    add r0, r4, 0x100
    ldrh r0, [r0, 0x3C] ; Var a...
    cmp r0, 0xFF ; This is the exit portal from brachyura...
    beq @@WarpOut
    pop r0
@@End:
    b 0x0203AFD0

@@WarpOut:
    ldr r0, = 0x020FFC8C
    ldr r2, [r0]
    bic r2, r2, 0x02 ; Clear the flag that we're in a boss fight
    str r2, [r0]
    pop r0
    ldr r0, = 0x021DD038
    mov r1, 0
    strb r1, [r0] ; Reset the music mute
    mov r2, 1
    mov r3, 0xA0
    strh r3, [r13]
    mov r3, 0x80
    mov r0, 0x09
    b @@End
;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; If we're refighting Albus, don't trigger the glyph cutscene again
@DontRespawnAlbusGlyph:
    cmp r0, 0
    bne 0x022B8DDC ; If in boss rush, ignore this completely
    mov r0, 0x35 ; Albus 3's location flag
    bl @CheckLocFlag
    b 0x022B8DB4 ; Let the game's own CMP handle this

; Prevent the game from trying to send us to the Boss Rush ending
@DontExitGame:
    cmp r0, 0x09 ; Final boss rush portal
    beq @@ResetOnNormal
@@End:
    bx lr
@@ResetOnNormal:
    push r0
    ldr r0, =0x02100790
    ldrb r0, [r0]
    cmp r0, 2 ; Boss Rush
    pop r0
    moveq r0, 9
    b @@End
;;;;;;;;;;;;;;;;;;;;;
;Determine where we go afte rBarlowe
@HandlePostBarloweFight:
    push r0
    ldr r0, = 0x0210038B
    ldrb r0, [r0]
    tst r0, 0x38  ; Flags that the Barlowe fight has been done before
    bne @@UndoFadeout
@@End:
    pop r0
    b 0x0203AFD0
@@UndoFadeout:
    ldr r0, = 0x0400006C
    push r1,lr
    mov r1, 0
    strb r1, [r0, r1]
    bl 0x02002CF4
    pop r1,lr
    b @@End
;;;;;;;;;;;;;;;;;;;;;;;
; Loads the value for Boss Chests
@GetBossChestItems:
    ldr r1, = @ROMTable_BossChestItems
    sub r0, r4, 1
    mov r0, r0, lsl 1 ; Shift it
    ldrh r1, [r1, r0] ; Load the value of this index
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;Locks boss doors
@LockBossDoor:
    add r0, r5, 0x100
    ldrh r0, [r0, 0x3E]
    cmp r0, 0x0F ; Dracula
    beq @@LockDraculaDoor
@@DontLockDoor:
    mov r0, r5
    b 0x02296B10
@@LockDraculaDoor:
    ldr r0, = @OptionFlag_BarloweRequired
    ldrb r0, [r0]
    cmp r0, 0
    beq @@DontLockDoor
    ldr r0, = 0x021003E4
    ldr r0, [r0]
    tst r0, 0x200 ; Barlowe's death flag
    bne @@DontLockDoor
    b 0x02297150 ; If we haven't beaten Barlowe, don;t open the door.
;;;;;;;;;;;;;;;;;;;;;;;;;
; Opens the map when Select is pushed
@RamFlag_MapTimer:
    .db 0x00
.align 4
@OneScreen_OpenMap:
    push lr
    bl 0x0203809C
    ldr r0, = @RamFlag_MapTimer
    ldrb r0, [r0]
    cmp r0, 0
    bne @@MapInit


    ldr r0, = 0x02101142
    ldrh r0, [r0]
    tst r0, 4 ; Select
    bne @@MapInit
@@End:
    pop lr
    bx lr
@@MapInit:

    ldr r0, = @OptionFlag_OneScreenMode
    ldrb r0, [r0]
    cmp r0, 0
    beq @@End
    ldr r0, = 0x02100A9C
    ldr r0, [r0]
    cmp r0, 0
    bne @@End ; Check a field of running fade timers. Don't open the map during a fade so it doesnt break after cutscenes...

    ldr r0, = 0x020FFC8C
    ldr r0, [r0]
    ldr r1, = 0x88100041 ; Dead, busy, pausing, or room transition
    tst r0, r1
    bne @@End ; If any of the above bits are set, dont open the map
    ldr r0, = 0x021000F4 ; Check if the player is frozen
    ldrb r0, [r0]
    cmp r0, 0
    bne @@End
    ldr r0, =0x020FFC8C
    ldr r1, [r0]
    orr r1, r1, 0x80 ; Hide the hud so that it doesnt display garbage
    str r1, [r0]

    ldr r0, =@RamFlag_MapTimer
    ldrb r1, [r0]
    add r1, r1, 1
    strb r1, [r0]
    cmp r1, 2
    blt @@End
    mov r1, 0
    strb r1, [r0] ; Reset the timer here


    ldr r1, = 0x020FFC58
    mov r0, 1
    strb r0, [r1, 0x49C]

    mov r0, 0x03
    strb r0, [r1, 0x49E]
    bl 0x0202D918


    ldr r0, = 0x020FFCB9
    ldrb r0, [r0]
    bl 0x02043480 ; Draw the map
    bl 0x0209DE14
    bl 0x02042CE4 ; Show the map
    mov r0, 1
    bl 0x020418A8
    b @@End

;;;;;;;;;;;;;;;;;
; Debug exit handler
@ExitDebugMap:
    tst r0, 0x07 ; Select, A, B
    bne @@MapClose
    b @@CheckTouch
@@MapClose:
    push r0,r1
    ldr r0, = 0x020FFC8C
    ldr r1, [r0]
    bic r1, r1, 0x80
    str r1, [r0] ; Unset the Hud Hide flag
    pop r0, r1
    bl 0x02045910
    mov r0, 0x63
    bl 0x0202D97C
    b 0x0203760C
@@CheckTouch:
    ldr r0, = 0x02101125
    ldrb r0, [r0]
    cmp r0, 0
    beq 0x0203760C ; Don't close the map unless the touch screen was only tapped

    ldr r0, =0x02101124
    ldrsh r1, [r0, 0x06] ; Check touch screen coordinates
    ldrsh r0, [r0, 0x04]
    cmp r0, 0x08
    blt 0x0203760C ; X must be higher than 8
    cmp r0, 0x18
    bgt 0x0203760C ; And lower than 18
    cmp r1, 0xA8
    blt 0x0203760C
    cmp r1, 0xB8
    bgt 0x0203760C
    b @@MapClose

@RamFlag_InMap:
    .db 0x00
.align 4
@DebugMap_DrawMarker:
    push lr
    ldr r0, = @RamFlag_InMap
    mov r1, 1
    strb r1, [r0]
    push r0
    ldr r0, = 0x0214B0F0
    mov r1, 0 ; Zero out the current selected warp
    strb r1, [r0]
    bl 0x02045A58 ; Draws the darkness effect. technically the area select handler
    mov r0, 1
    bl 0x0204247C
    pop r0
    mov r1, 0
    strb r1, [r0]
    pop lr
    bx lr


; Get the player's X instead of warp room x
@DebugMap_DrawX:
    ldr r2, = @RamFlag_InMap
    ldrb r2, [r2]
    cmp r2, 0
    beq @@NormalDraw
    ldr r2, = 0x020FFCB0 ; Player's X
    bx lr
@@NormalDraw:
    ldr r2, = 0x0214B0C7
    bx lr

; Get the player's y instead of warp room y
@DebugMap_DrawY:
    ldr r2, = @RamFlag_InMap
    ldrb r2, [r2]
    cmp r2, 0
    beq @@NormalDraw
    ldr r2, = 0x020FFCB4 ; Player's y
    bx lr
@@NormalDraw:
    ldr r2, = 0x0214B0C8
    bx lr

; Skips over other map logic
@DebugMap_Close:
    ldr r1, =@RamFlag_InMap
    ldrb r1, [r1]
    cmp r1, 1
    beq 0x020460FC
    ldrh r1, [r0, 0x02]
    b 0x02045D0C

; Skips some logic from area exits that ignores the map
@DebugMap_SkipWarpLogic:
    cmp r0, 1
    bne 0x02045C80
    ldr r0, = @RamFlag_InMap
    ldrb r0, [r0]
    cmp r0, 1
    beq 0x02045C80
    b 0x02045C14

; Same as above
@DebugMap_SkipLogic2:
    cmp r0, 0
    bne 0x02045C08
    ldr r0, = @RamFlag_InMap
    ldrb r0, [r0]
    cmp r0, 1
    beq 0x02045C08
    b 0x02045A7C
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Disable switching to the Map Screen in Onescreen mode
@OneScreen_DisableScreenSwap:
    ldr r0, = @OptionFlag_OneScreenMode
    ldrb r0, [r0]
    cmp r0, 0
    bxne lr
    mov r0, r4
    b 0x020657F8
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Turns off Volaticus when entering the Minera boss room so we don't softlock
@SkeletonFlightDisable:
    ldr r0, = 0x021002C4
    ldrh r0, [r0] ; Get the current R glyph
    cmp r0, 3 ; Check if it's Volaticus
    bne @@End
    push lr
    bl 0x0204DFB8 ; Disable the glyph if it is
    pop lr
@@End:
    mov r3, 0x5200
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Gives the player +1 to all AP points when getting an arbitrary glyph
@GetGlyphAP:
    cmp r0, 0x70
    bge @@End ; Any non-glyph
    push r0-r2
    ldr r0, = 0x0210031C
    mov r2, 0
@@GetNextPoint:
    ldrh r1, [r0, r2]
    add r1, r1, 1 ; +1 AP point
    strh r1, [r0, r2]
    cmp r2, 0x0C
    bge @@ExitLoop
    add r2, r2, 2
    b @@GetNextPoint
@@ExitLoop:
    pop r0-r2
@@End:
    bx lr
;;;;;;;;;;;;;;;;;;;;;;
; If the castle is already open, don't show the castle cutscene
@PostBarloweWarp:
    ldr r0, = @OptionFlag_OpenCastle
    ldrb r0, [r0]
    cmp r0, 0
    bne @@NewWarp
    mov r0, 0x13
    b 0x0203AFD0
@@NewWarp:
    ldr r0, = 0x0210038B
    ldrb r1, [r0]
    orr r1, r1, 0x10
    strb r1, [r0] ; Set the flag that we watched that cutscene
    mov r0, 0xB0
    strh r0, [r13]
    mov r0, 0x02
    mov r1, 0x00
    mov r2, 0x06
    mov r3, 0x140
    b 0x0203AFD0
;;;;;;;;;;;;;;;;;;;
; Stop the game from setting the recent top type
@OneScreen_DontResetTopType:
    ldr r0, = @OptionFlag_OneScreenMode
    ldrb r0, [r0]
    cmp r0, 0
    bne @@ForceStatus
@@End:
    ldr r0, = 0x020FFC58
    bx lr
@@ForceStatus:
    mov r4, 7
    b @@End
;;;;;;;;;;;;;;;;;;;
; If a villager's glyph would have a negative Y-pos (I.e. it's out of bounds off the top of the map), clamp it to Y 0 instead
@ClampVillagerGlyphPos:
    cmp r1, 0
    movle r1, 0 ; If less than 0, clamp at 0
    b 0x0206DDEC
;;;;;;;;;;;;;;;;;;;
; Necromancer needs to set r3 glyph flag here so it doesn't override other things
@SetNecromancerGlyph:
    mov r3, 0x03
    stmfa [r13], r0, r3
    b 0x0224E8B8
;;;;;;;;;;;;;;;;;;;;
; Checks if we've set the Flag for an enemy's Glyph (obtained it). r6 Enemy ID. returns 1 in r0 if we have.
@CheckIfEnemGlyphObtained:
    ldr r0, = @ROMTable_EnemyGlyphIndex
    mov r1, 0
@@CheckIndexNext:
    ldrb r2, [r0, r1]
    cmp r2, r6 ; Check if the current Index == the current enemy ID
    beq @@GotEnemyIndex
    cmp r1, @EnemGlyphIndex_len ; If we've exhausted the whole table...
    bge @@Exit_SetFail ; Count this as a fail...? Does this code even get run? delete if not
    add r1, r1, 1
    b @@CheckIndexNext
@@GotEnemyIndex:
    ldr r0, = @ROMTable_EnemyGlyphFlags
    mov r1, r1, lsl 1 ; Shift
    ldrh r0, [r0, r1] ; use R1 counter value from the previous loop to look up which flag this is
    push lr
    bl @CheckLocFlag ; Check if this FLAG is set
    pop lr ; 0 Is the result of the LOC flag, so we don't need anything else
    bx lr
@@Exit_SetFail:
    mov r0, 0 ; Force a failure
    bx lr

; Used to determine if an enemie's drops have been 100% collected outside of its bestiary page
@CheckIfEnemGlyphObtained_BestMain:
    push r6, lr
    add r6, r10, r1
    bl @CheckIfEnemGlyphObtained
    pop r6, lr
    bx lr
;;;;;;;;;;;;;;;;;;;;;;
; Set flag r3
@SetSpearGuardGlyph:
    mov r0, r6
    mov r3, 0x08
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;
; glyph flag re
@SetWerebatGlyphFlag:
    mov r3, 0x12
    str r3, [r13, 0x0C]
    bx lr
;;;;;;;;;;;;;;;;;;;;;;;;;
@SetDullahanGlyphFlag:
    mov r3, 0x16
    str r3, [r13, 0x0C]
    bx lr

@SetMissMurderGlyphFlag:
    mov r3, 0x19
    str r3, [r13, 0x0C]
    bx lr

@SetLizardmanGlyphFlag:
    mov r3, 0x1C
    str r3, [r13, 0x0C]
    bx lr

@SetPantherGlyphFlag:
    mov r1, 0x2A
    str r1, [r13, 0x0C]
    bx lr

; Black and White Fomors both set this same code path, so we need to differentiate them
@SpawnFomorGlyph:
    push r1
    add r13, r13, 4
    cmp r3, 0x45 ; White
    moveq r1, 0x27
    movne r1, 0x14 ; Black
    str r1, [r13, 0x08]
    sub r13, r13, 4
    pop r1
    b 0x0206DEE0

@SetPolkirGlyphFlag:
    mov r3, 0x2B
    str r3, [r13, 0x0C]
    bx lr

@SetSpecSwordGlyphFlag:
    mov r3, 0x36
    str r3, [r13, 0x0C]
    bx lr

@SetAutomatonGlyphFlag:
    mov r3, 0x37
    str r3, [r13, 0x0C]
    bx lr

@SetGreatKnightGlyphFlag:
    mov r3, 0x39
    str r3, [r13]
    bx lr
;;;;;;;;;;;;;;;;;;;;;;
; Spawn's Barlowe's Glyph in case you missed it the first time
@SpawnBarloweMissedGlyph:
    ldr r0, = @OptionFlag_StolenGlyphChecks
    ldrb r0, [r0] ; We don't need to do this if it's not a Check
    cmp r0, 0
    beq @@Exit
    ldr r0, = 0x021003E4
    ldr r0, [r0]
    tst r0, 0x200
    beq @@Exit ; We only want to do this if Barlowe isn't alive

    mov r0, 0x7C
    push lr
    bl @CheckLocFlag ; Check if we've already gotten the Glyph
    cmp r0, 1
    beq @@ExitAndPop ; Don't spawn it if we already got it
    push r1-r3
    mov r0, -1
    str r0, [r13] ; Glyph spawn timer
    mov r0, 0
    str r0, [r13, 4] ; Set Glyph as active
    mov r0, 0x7C ; Barlowe's Glyph Flag
    str r0, [r13, 0x08]
    
    ldr r1, =0x55000 ; Y pos
    ldr r2, = 0x6000
    mov r3, 0x73 ; Barlowe
    mov r0, 0x100000 ; X pos
    bl 0x0206DEE0 ; Spawn Barlowe's glyph
    pop r1-r3
@@ExitAndPop:
    pop lr
@@Exit:
    ldr r0, = 0x020FFC58
    bx lr
;;;;;;;;;;;;;;;;;;;;;;
; Same as the above but for Albus
@SpawnAlbusMissedGlyph:
    ldr r0, = @OptionFlag_StolenGlyphChecks
    ldrb r0, [r0]
    cmp r0, 0
    beq @@Exit
    ldr r0, = 0x021003E4
    ldr r0, [r0]
    tst r0, 0x100
    beq @@Exit ; We only want to do this if Albus isn't alive
    ldr r0, = 0x02100388
    ldr r0, [r0]
    tst r0, 0x02000000
    beq @@Exit  ; Make sure that we've cleared all the events out of this room first


    mov r0, 0x63
    push lr
    bl @CheckLocFlag
    cmp r0, 1
    beq @@ExitAndPop
    push r1-r3
    mov r0, -1
    str r0, [r13]
    mov r0, 0
    str r0, [r13, 4]
    mov r0, 0x63
    str r0, [r13, 0x08]

    ldr r1, =0x55000 ; Y pos
    ldr r2, = 0x6000
    mov r3, 0x72 ; Albus
    mov r0, 0x100000 ; X pos
    bl 0x0206DEE0 ; Spawn Albus's glyph
    pop r1-r3
@@ExitAndPop:
    pop lr
@@Exit:
    ldr r0, = 0x020FFC58
    bx lr
;;;;;;;;;;;;;;;;;;;;;
; Clears deathlink data upon loading into a save
@CreateAndClearDeaths:
    push lr
    bl 0x0204E6D8
    push r0
    ldr r0, = @RAMFlag_ReceivedServerDeath
    ldrb r1, [r0]
    tst r1, 0x02 ; Flag that a death has already been processed
    beq @@SkipClear
    mov r1, 0
    strb r1, [r0]
@@SkipClear:
    pop r0
    pop lr
    bx lr

@RemoteKillPlayer:
    push lr
    bl 0x0208C6BC
    ldr r0, = @RAMFlag_ReceivedServerDeath
    ldrb r1, [r0]
    tst r1, 0x01 ; Flag that we received a death from the server
    beq @@Exit
    ;;;;;;;;;;;;;;;;;;
    ;State checker
    ldr r0, = 0x02100A9C
    ldr r0, [r0]
    cmp r0, 0
    bne @@Exit ; Check a field of running fade timers. Don' kill during a fade so it doesnt break after cutscenes...
    ldr r0, = 0x020FFC8C
    ldr r0, [r0]
    ldr r1, = 0x88100041 ; Dead, busy, pausing, or room transition
    tst r0, r1
    bne @@Exit ; If any of the above bits are set, ignore
    ldr r0, = 0x021000F4 ; Check if the player is frozen
    ldrb r0, [r0]
    cmp r0, 0
    bne @@Exit
    ;;;;;;;;;;;;;;;;;;
    ldr r0, = @RAMFlag_ReceivedServerDeath
    mov r1, 0x02 ; Set the processed flag
    strb r1, [r0]
    ldr r0, = 0x020FFC8C
    ldr r1, [r0]
    orr r1, r1, 0x40
    str r1, [r0] ; Kill the player
    ldr r0, = 0x21002B4
    mov r1, 0
    strh r1, [r0] ; Zero out the player's HP for the death transition
@@Exit:
    pop lr
    bx lr
;;;;;;;;;;;;;;;;;;
; Switches the pointer we were going to load with the one for fsha04
@SwapLoadedGlyphPointer:
    push r0
    ldr r0, = @RamFlag_ExtendedGlyphID
    ldrh r0, [r0]
    cmp r0, 0
    beq @@End
    ldr r1, = 0x020E1E72
@@End:
    pop r0
    b 0x0200BDC8

.pool
.endarea
.close


; Money is items 0x161-167
; Villagers are 168-175
; Map ids are 176 and above
