.nds
.relativeinclude on
.erroronwarning on

@Overlay41Start equ 0x02308920
@FreeSpace equ @Overlay41Start + 0x50

@SoulFlagTable equ 0x02308930
@ServerItemType equ 0x02308940
@SkipNameShowFlag equ 0x02308942
@TotalItemsReceived equ 0x0230894E


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/arm9.bin", 02000000h
;;Fixes ability souls setting other bits unintentionally
.org 0x0202E258
  b 0202E300h

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

.org 0x0203008C
    bl @GetItemFromServer

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x02010BCC
    bl @LoadAPData

.org 0x020111B8
    bl @SaveAPData

.close
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.open "ftc/overlay9_0", 0219E3E0h

.org 0x021E9674
    bl @ToggleSoulFlag

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021D7B1C
    bl @FilterItemFlagHigh

.org 0x021E8A48
    bl @FilterWriteFlagHigh

.org 0x021E897C
    b @SpecialItemHandler ;This is normally the GetItem call in the get consumable func

.org 0x021E8AA8
    bl @SkipShowName

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021EEED4
    b @WarpToStart

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021E9640
    b @GetItemFromSoul
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021F60B4
    b @GiveStartingInventory

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021AF560
;Special/trigger items need to be handled differently, since they don't run the touch pickup code
bl @FilterSpecialItemFlagHigh

.org 0x021AFA28 ;Stop these items from being given by the original code
nop

.org 0x021AFA30
bl @GetItemFromSpecial

;;;;;;;;;;;;;;;;;;;;;;;;
.org 0x021CEBEC
b @CeliaEventHandler
.close
.open "ftc/overlay9_41", @Overlay41Start

.org @FreeSpace
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    @SoulTypeTable:
    .dh 0x500
    .dh 0x501
    .dh 0x502
    .dh 0x503
    .dh 0x504
    .dh 0x505
    .dh 0x506
    .dh 0x507
    .dh 0x508
    .dh 0x509
    .dh 0x50a
    .dh 0x50b
    .dh 0x50c
    .dh 0x50d
    .dh 0x50e
    .dh 0x50f
    .dh 0x510
    .dh 0x511
    .dh 0x512
    .dh 0x513
    .dh 0x514
    .dh 0x515
    .dh 0x516
    .dh 0x517
    .dh 0x518
    .dh 0x519
    .dh 0x51a
    .dh 0x51b
    .dh 0x51c
    .dh 0x51d
    .dh 0x51e
    .dh 0x51f
    .dh 0x520
    .dh 0x521
    .dh 0x522
    .dh 0x523
    .dh 0x524
    .dh 0x525
    .dh 0x526
    .dh 0x527
    .dh 0x528
    .dh 0x529
    .dh 0x52a
    .dh 0x52b
    .dh 0x52c
    .dh 0x52d
    .dh 0x52e
    .dh 0x52f
    .dh 0x530
    .dh 0x531
    .dh 0x532
    .dh 0x533
    .dh 0x534
    .dh 0x535
    .dh 0x536
    .dh 0x537
    .dh 0x538
    .dh 0x539
    .dh 0x53a
    .dh 0x53b
    .dh 0x53c
    .dh 0x53d
    .dh 0x53e
    .dh 0x53f
    .dh 0x540
    .dh 0x541
    .dh 0x542
    .dh 0x543
    .dh 0x544
    .dh 0x545
    .dh 0x546
    .dh 0x547
    .dh 0x548
    .dh 0x549
    .dh 0x54a
    .dh 0x54b
    .dh 0x54c
    .dh 0x54d
    .dh 0x54e
    .dh 0x54f
    .dh 0x550
    .dh 0x551
    .dh 0x552
    .dh 0x553
    .dh 0x554
    .dh 0x555
    .dh 0x556
    .dh 0x557
    .dh 0x558
    .dh 0x559
    .dh 0x55a
    .dh 0x55b
    .dh 0x55c
    .dh 0x55d
    .dh 0x55e
    .dh 0x55f
    .dh 0x560
    .dh 0x561
    .dh 0x562
    .dh 0x563
    .dh 0x564
    .dh 0x565
    .dh 0x566
    .dh 0x567
    .dh 0x568
    .dh 0x569
    .dh 0x56a
    .dh 0x56b
    .dh 0x56c
    .dh 0x56d
    .dh 0x56e
    .dh 0x56f
    .dh 0x570
    .dh 0x571
    .dh 0x572
    .dh 0x573
    .dh 0x574
    .dh 0x575
    .dh 0x576
    .dh 0x577
    .dh 0x578
    .dh 0x579
    .dh 0x57a
.align 4
;;;;;;;;;;;;;;;;
@OptionFlag_FightMenace:
    .db 0x00
.align 4
;;;;;;;;;;;;;;
@Romname_AP:
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
    .dh 0xFFFF
.align 4
    ;Dedicate 0x20 bytes to the AP rom name.

;   Convert souls to a Bitfield table to indicate that that soul has been obtained once
    @ToggleSoulFlag:
    push r0 ;Backup the ID number
    push r1
    push lr
    bl @GetSoulFlagFromID
    ldr r11, =@SoulFlagTable
    mov r12, r0
    ldrb r0, [r11, r0]; The divided soul id is the index
    orr r0, r0, r1
    strb r0, [r11, r12]
    pop lr
    pop r1
    pop r0
    bx lr
    .pool

    @ToggleSoulFlagDummyChange:
    ldr r12, =@SoulFlagTable
    str r1,[r12,r0,lsl 2h]
    ldr r12, =0x020F70D0
    str r1,[r12,r0,lsl 2h]
    bx lr
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Returns the index and bit to check from the soul table
    @GetSoulFlagFromID:
    push lr
    ldr r1, =0x08
    bl 0x02075B28 ; Divide soul id by 8
    ldr r11, = 0x01
    lsl r1, r11, r1
    pop lr
    bx lr
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Get an item from the Server. What this does is take Item Type 0, Item ID 1,
    ;and gives it to the player. Type 5 is souls. AP server items fill these values
@MoneyValues:
.dh 0x0001, 0x000A, 0x0032, 0x0064, 0x01F4, 0x03E8, 0x07D0
.align 4


@GetItemFromServer:
    push lr
    ldr r0, =0x020CAA24
    ldrb r0, [r0, 0]
    cmp r0, #1 ;This usually means we're in text or something
    beq @GetItemFinished
    ldr r0, =0x020F6DFC
    ldr r0, [r0, 0]
    and r0, r0, 0xFFFFFFF6 ;Dont check items in events or getting a Seal

    ldr r0, =@ServerItemType ;Get the current item type
    mov r2, r0
    ldrb r0, [r0]
    cmp r0, #0
    beq @GetItemFinished
    add r2, r2, #1
    ldrb r1, [r2] ;R0 = item type, R1 = item ID
    cmp r0, #5
    beq @GetSoul
@GetItem:
    bl @GetItemArbitrary
@CleanupItems:
    ldr r1, =@ServerItemType
    ldr r2, =0x00
    strb r2, [r1]
    b @GetItemFinished
    .pool
@GetSoul:
    bl @GetSoulArbitrary
    b @CleanupItems

@GetItemFinished:
    pop lr
    b 0x020213EC

@GetItemArbitrary:
    push lr
    cmp r0, #1 ;Is this money?
    beq @GetMoneyArbitrary
    cmp r0, #2
    bne @CheckForSeal
    cmp r1, #0x3C
    bgt @GetMagicSeal
@CheckForSeal:
    push r0-r1
    bl 0x021E7870 ;GiveItem

    pop r0-r1
    bl 0x021E7AB4 ;GetGlobalItemID+1
    ldr r1, =0xF0
    bl 0x0202DE80 ;ShowItemName

    ldr r0, =0x149
@PlaySoundFromItem:
    bl 0x02029BF0 ;PlaySound
    
    pop lr
    bx lr
    .pool
@GetMoneyArbitrary:
    ldr r0, =@MoneyValues
    mov r1, r1, lsl #1 ;Load the amount of money
    ldrh r0, [r0, r1]
    push r0
    bl 0x021E76D4 ;Function to give money
    pop r0
    ldr r1, =0xF0
    bl 0x0202DDC4 ;DisplayMoneyCount
    ldr r0, =0x01B1
    b @PlaySoundFromItem
    .pool
@GetMagicSeal:
    push r0-r1
    sub r1, r1, 0x3D
    ldr r0, =0x01 
    lsl r0, r0, r1 ;Get the proper bit for the Seal
    ldr r1, =0x020F7254
    ldrb r2, [r1, 0]
    orr r0, r2
    strb r0, [r1, 0]
    pop r0-r1
    b @CheckForSeal
    .pool

@GetSoulArbitrary:
    mov r0, r1
    push lr
    push r0
    cmp r0, #0x74
    blt @GiveNormalSoul
    bl @ActivateAbilitySoul
@GiveNormalSoul:
    ldr r1, =0xF0
    bl 0x0202E184 ;ShowSoulName
    pop r0
    push r0
    bl 0x0221029C ;GetNumSoul
    mov r1, r0
    cmp r0, #9 ;Do we have 9 of this soul?
    beq @SkipSoulInc
    add r1, r0, #1
    @SkipSoulInc:
    pop r0
    bl 0x02210208 ;Get Soul
    ldr r0, =0x30
    bl 0x02029BF0 ;PlaySound
    pop lr
    bx lr
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Filters the high byte out of an item's flag when trying to spawn it.
@FilterItemFlagHigh:
    and r3, r3, 0xFF
    mov r1, 0x01
    bx lr

;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Prevents items from writing the high byte of their flag
@FilterWriteFlagHigh:
    ldr r12,[r0,0x6E]
    and r12, r12, 0xFF
    bx lr

;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Handles things like picking up AP items, and the Soul Can item.
@SpecialItemHandler:
    cmp r0, 0x02 ;We should only check this for consumables
    beq @GiveSpecial
@GiveNormal:
    bl 0x021E7870
    b 0x021E8980
@GiveSpecial:
    cmp r1, 0x3A
    blt @GiveNormal ;Only 3A-3C are Special items.
    cmp r1, 0x3C
    beq @GiveSoulCan
    b 0x021E8988 ;AP items dont go into the inventory, so we skip adding them
@GiveSoulCan:
    ldrb r1, [r9, 0x026F] ; The high byte of the item's flag is used as the soul ID
    bl @GetSoulArbitrary
    ldr r1, =@SkipNameShowFlag
    ldr r0, =0x1
    ldr r4, =0x00
    strb r0, [r1, 0]

    b 0x021E89EC ;End the item handler
;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Causes the Castle Map 0 item to warp the player to the starting room
@WarpToStart:
    ldrb r2, [r8, 0]
    cmp r2, #0x2B ;Is this Castle Map 0?
    beq @UseWarp
@NormalUse:
    ldrb r2, [r8, 0x08]
    b 0x021EEED8
@UseWarp:
    ldr r1, =0x020F6DFC
    ldr r1, [r1, 0]
    and r1, r1, 0xB7FFFFFF ;Filter out all game state bits except for Paused and No Save
    and r1, r1, 0xCF
    cmp r1, 0x0
    bne @NormalUse
    ldr r1, =0x020F6DF9
    ldrb r1, [r1, 0]
    cmp r1, 0x0
    bne @NormalUse ;Don't use warp while in the mirror world
    push lr
    ldr r0, =0x00
    ldr r1, =0x01
    ldr r3, =0xA0
    ldr r2, =0x0100 ;This is the area/room/position. if i want to change starting room later ill have to edit these
    bl 0x02026AD0 ;Set Warp Dest
    ldr r1, =0x020F6DF4
    ldr r0, =0x6
    strb r0, [r1] 
    ldr r0, =0x0
    strb r0, [r1,1]
    bl 021F64BCh ;Enable controls
    ldr r0, =0x30
    bl 0x02029BF0 ;PlaySound
    pop lr
    b 0x021EF28C
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Overrides the function that gives the player a Soul normally. We interject here so I can call my arbitrary item giving funcs
@GetItemFromSoul:
    push lr
    push r0-r2
    bl @ToggleSoulFlag
    pop r0-r2

    ldr r2, =@SoulTypeTable
    mov r0, r0, lsl # 1
    ldrh r1, [r2, r0] ;Look up the item
    and r0, r1, 0xFF00
    and r1, r1, 0x00FF
    lsr r0, r0, 8
    cmp r0, #0x05
    beq @GetSoulSoul
    bl @GetItemArbitrary
    b @SoulGetFinish
@GetSoulSoul:
    bl @GetSoulArbitrary
@SoulGetFinish:
    pop lr
    b 0x021E96B0
    .pool
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Give the starting weapon + Return Gem
@GiveStartingInventory:
    bl 0x021E78F0 ;Set Item Count
    ldr r0, =0x02
    ldr r1, =0x2B
    bl 0x021E78F0
    ldr r0, =0x020F7420 ;Starting weapon
    ldrb r1, [r0, 0]
    ldr r0, =0x03
    bl 0x021E78F0
    b 0x021F60B8
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Transfers AP data in and out of saved memory
    ;0x0A001F00 for testing
@LoadAPData:
    push r0-r3
    push lr
    ldr r1, =0x1F00
    mov r0, r0, lsl #5
    add r0, r0, r1
    ldr r1, =@SoulFlagTable
    ldr r2, =0x20
    ldr r3, =0x00
    bl 0x020684E0 ;WriteToSaveData
    pop lr
    pop r0-r3
    b 0x02010C7C
    .pool

@SaveAPData:
    push r0-r3
    push lr
    mov r2, r9, lsl #5
    ldr r0, =0x1F00
    add r0, r0, r2
    ldr r1, =@SoulFlagTable
    ldr r2, = 0x20
    bl 0x02068410
    pop lr
    pop r0-r3
    b 0x2011F3C
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Activates Ability Souls when getting them
@ActivateAbilitySoul:
    push r0-r2
    sub r0, r0, 0x74 ;if getting an Ability soul, activate it
    ldr r1, = 0x01
    lsl r0, r1, r0 ;Translate the id to a bit
    ldr r1, =0x20F741E
    ldrb r2, [r1, 0]
    orr r0, r0, r2
    strb r0, [r1, 0]
    pop r0-r2
    bx lr
    .pool

    ;Saving data is 0x02068410. r0 = offset, r1 = source, r2 = count. r9 = file number
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
@FilterSpecialItemFlagHigh:
    ldr r12,[r1,0x70]
    and r12, r12, 0xFF
    bx lr

@GetItemFromSpecial:
    ldr r12, [r0, 0x70]
    push r0-r1
    push lr
    push r12
    ldrb r1, [r4, 0x0F]
    mov r3, r12
    and r3, r3, 0xFF00
    lsr r3, r3, 0x08
    cmp r3, #5
    beq @GetSpecialSoul
    mov r0, r3
    bl @GetItemArbitrary
    b @SpecialCleanup
@GetSpecialSoul:
    bl @GetSoulArbitrary
@SpecialCleanup:
    pop r12
    and r12, r12, 0xFF
    pop lr
    pop r0-r1
    bx lr

    ;For the specials, i dont think i can change the sprite (for now)
    ;Change the item ID in the global Special Item table. This var also acts as the Soul ID.
    ;spawner is at 0x021AF558
    ;It's definitely at 0x021F5A8. this calls LoadSpriteSingleGFX. But how does it work...?
    ;r3 is the Palette Index

;;;;;;;;;;;;;;;;;;;;;;;
@SkipShowName:
    push r0-r1
    ldr r1, =@SkipNameShowFlag
    ldrb r0, [r1, 0]
    cmp r0, #0
    bne @SkipName
    pop r0-r1
    b 0x0202DE80
@SkipName:
    ldr r0, =0x0
    strb r0, [r1, 0]
    pop r0-r1
    b 0x021E8AAC
    .pool

;;;;;;;;;;;;;;;;;;;;;;;;
@CeliaEventHandler:
    cmp r0, 0x0
    beq @DeleteCelia
    ldr r1, =@OptionFlag_FightMenace
    ldrb r1, [r1, 0]
    cmp r1, #0 ;Menace+ is disabled
    beq @CeliaEnd
@CheckMenacePlus:
    ldr r1, =0x20F7039
    ldrb r0, [r1, 0]
    and r0, r0, 0x08 ;Is Aguni defeated?
    cmp r0, #0
    beq @DeleteCelia
    b 0x021CEC08
@DeleteCelia:
    b 0x021CEBF4
@CeliaEnd:
    b 0x021CEC08
    .pool
    .close

;TODO. make sure Return Gems dont work in bosses

;Todo. maybe kill the player if they go out of bounds
;If map coordinates (y anyways) are > A0, kill player



;AP todo. Options, make a basepathc,
;todo. determine we're actually in-game
