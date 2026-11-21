#IncSrc "apc2_get_items.asm"

#org $AABE, $12ACE
    INC $04EF
    RTS

#org $AAC6, $12AD6
LoadGame:
    LDX #$0F
.Loop:
    LDA $6000,X
    STA $0540,X
    DEX
    BPL .Loop
    JMP LoadIntoFile
    RTS

#org $AD47, $12D57
    JMP $AD4D

#org $ADB6, $12DC6
    LDA #$00
    STA $19
    RTS

#org $ADC8, $12DD8
    INC $04EF
    RTS

#org $ADD6, $12DE6
SaveGame:
    LDX #$0F
.SaveLoop:
    LDA $0530,X
    CLC
    ADC #$01
    STA $6000,X
    DEX
    BPL .SaveLoop
    JMP SaveIntoFile
; Code for the SRAM Patch
;;;;;;;;;;;;;;;;;;;;;;;;;
#org $BA1D, $13A2D
    ; Load text for the title screen
    #byte $0C, $0F, $01, $04, $00, $00, $00, $00

#org $C984, $1C994
    ; Save text for the death screen
    #byte $13, $01, $16, $05, $00, $00, $00, $00
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 ; Prevent the game from checking the life counter when dying; infinite lives
#org $C294, $1C2A4
    JMP LoadSaveMenu
;;;;;;;;;;;;;;;;;;;;
; Disable the life counter on the load-in screen.
; The PLAYER text
#org $C962, $1C972
    #byte $00, $00, $00, $00, $00, $00

; The life number
#org $CC75, $1CC85
    LDA #$00
    NOP
    NOP
    NOP
;;;;;;;;;;;;;;;;;;;;;;;
#org $EE9D, $1EEAD
    LDA #$00 ; Make the text speed instant

;;;;;;;;;;;;;;;;;;;;
#org $C314, $1C324
    NOP ; Prevent the game from zeroing the Heart count on game over
    NOP
    NOP
;;;;;;;;;;;;;;;;;;;;
#org $D949, $1D959
    NOP ; Prevent the game from removing Oak Stake when used
    NOP

#org $D95C, $1D96C
    NOP ; Prevent the game from automatically unequipping oak stake
    NOP
;;;;;;;;;;;;;;;;;;;;
#org $CF1B, $1CF2B
    LDA #$01 ; Shorten the time day fades take

#org $CECF, $1CEDF
    INC $88
    BNE $CED8 ; Set the blackout to end immediately

;#org $D7DB, $1D7EB
 ;   LDA #$05 ; Skip the day/night text
;;;;;;;;;;;;;;;;;;;;;
#org $AD69, $12D79
    NOP ; Don't zero out hearts on a reload
    NOP
    NOP

#org $AD61, $12D71
    NOP ; Don't zero out selected sub
    NOP

#org $AD63, $12D73
    NOP ; Don't zero out selected relic
    NOP
;;;;;;;;;;;;;;;;;;;;
#org $AE88, $12E98
    NOP ; Loading would normally reject Impossible Flags for items (like bit 0x80 of Relics)
    NOP ; I want these to be set, so ignore this
;;;;;;;;;;;;;;;;;;;;
#org $F27B, $1F28B
    AND #$E0 ; Allow the game to see bit 0x80 as a Crystal for menu selection
;;;;;;;;;;;;;;;;;;;
#org $9088, $5098
    JMP CheckBlueCrystalTrader
;;;;;;;;;;;;;;;;;;;;;
#org $8799, $47A9
    NOP
    NOP ; Prevent the game from writing in Drac relics
;;;;;;;;;;;;;;;;;;;;;
; Cap hearts at 9999
#org $8862, $4872
    CMP #$99

#org $8868, $4878
    CMP #$99

#org $886C, $487C
    LDA #$99
;;;;;;;;;;;;;;;;;
#org $8C77, $4C87
    BCC $8C85 ; Flame whip as well as morning star
    JMP SetFlameWhipCheck

#org $8C81, $4C91
    NOP
    NOP ; Don't set the txt id here
;;;;;;;;;;;;;;;;;;
#org $87BF, $47CF
    JMP $87D3 ; Skip writing in the cross and stuff
;;;;;;;;;;;;;;;;;;
#org $907F, $508F
    LDA #$56 ; Change the crystal obtained text for the Aljiba guy
;;;;;;;;;;;;;;;;;;
#org $87C9, $47D9
    NOP ; Skip golden knife
    NOP

#org $9883, $D893
    ;I LIKE YOUR JIB.
    ; NOW TAKE
    ; THIS JUNK.
    #byte $09, $00, $0C, $09, $0B, $05, $00, $19
    #byte $0F, $15, $12, $FE, $0A, $09, $02, $1B
    #byte $00, $0E, $0F, $17, $00, $14, $01, $0B
    #byte $05, $FE, $FA, $1B, $FF, $13, $00, $0A
    #byte $15, $0E, $0B, $1B, $FF

; AP logo sprite for menus
#org $200, $20210
#incbin "apc2_apitem.bin"

; Letter sprite over books, repeated in several graphic banks
#org $420, $20430
#incbin "apc2_letter_spr.bin"

#org $420, $22430
#incbin "apc2_letter_spr.bin"

#org $420, $24430
#incbin "apc2_letter_spr.bin"

#org $420, $26430
#incbin "apc2_letter_spr.bin"

#org $420, $28430
#incbin "apc2_letter_spr.bin"

#org $420, $2B430
#incbin "apc2_letter_spr.bin"
;;;;;;;;;;;;;;;;;;;;;;;
#org $87CD, $47DD
    JMP $87D3 ; Don't activate the fire item



;;;;;;;;;;;;;;;;;;;
#org $CC2A, $1CC3A
    JSR TriggerManualDeath
;;;;;;;;;;;;;;;;;;;
#org $D774, $1D784
    JMP GetItemFromServer
;;;;;;;;;;;;;;;;;;;
#org $EC98, $1ECA8
    JMP StockAtChurch
;;;;;;;;;;;;;;;;;;;
#org $F2F6, $1F306
    JMP ProcessExtraMenuInputs
;;;;;;;;;;;;;;;;;;;
#org $F024, $1F034
    JMP CrystalSetColor
;;;;;;;;;;;;;;;;;;;
#org $85FE, $460E
    JMP CheckBespokeCrystalWhite
;;;;;;;;;;;;;;;;;;;
#org $A793, $67A3
    JMP CheckBespokeCrystalBlue
;;;;;;;;;;;;;;;;;;
#org $EFC8, $1EFD8
    JMP ReloadCrystalGFX
;;;;;;;;;;;;;;;;;
#org $A93C, $694C
    JMP CheckBespokeCrystalRed
;;;;;;;;;;;;;;;;;
#org $C232, $1C242
    JSR InitializeNewGameData
;;;;;;;;;;;;;;;;;
#org $8162, $4172
    JSR LogCheckID ; NPCS
;;;;;;;;;;;;;;;;;
#org $8725, $4735
    JMP StoreCurrentCheck
;;;;;;;;;;;;;;;;;
#org $ED9E, $1EDAE
    JMP SetMerchantCheck
;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;
#org $AE03, $6E13
    LDA #$10 ; Graveyard duck
    STA $7F
    JSR SetNPCTalkToCheck
    JMP $AE0D
;;;;;;;;;;;;;;;;
#org $ECE4, $1ECF4
    JMP LoadItemIcon
;;;;;;;;;;;;;;;
#org $8112, $4122
    JSR HandleBookChecks ; Books are ID 27 at 17
;;;;;;;;;;;;;;
#org $87A0, $47B0
    JMP SetBookCheck
;;;;;;;;;;;;;;
#org $ADC2, $6DD2
    JMP CheckBespokeCrystalBlue_2
;;;;;;;;;;;;;;
#org $934B, $535B
    JSR SetNPCTalkToCheck ; Free laurel guy in Mansion 5
    JMP $935D
;;;;;;;;;;;;;;
#org $AE12, $6E22
    LDA #$10
    STA $7F
    JSR SetNPCTalkToCheck
    JMP $AE1C
;;;;;;;;;;;;
#org $9075, $5085
    JMP SetCrystalTraderCheck
;;;;;;;;;;;;
#org $EF0A, $1EF1A
    JMP SetNothingSounds
;;;;;;;;;;;;;;;;;;;;;;;
#org $AA3A, $6A4A
    LDA #$12
    STA $7F
    JSR SetNPCTalkToCheck
    RTS
;;;;;;;;;;;;;;;;;;;;;;;;
#org $EEB8, $1EEC8
    JMP GetDynamicItemName
;;;;;;;;;;;;;;;;;;;;;;;
#org $EEA4, $1EEB4
    JMP GetDynaTexPointr
;;;;;;;;;;;;;;;;;;;;;;;
#org $ED90, $1EDA0
    JMP MerchantNonRenewableCheck
;;;;;;;;;;;;;;;;;;;;;;;
#org $ED70, $1ED80
    JMP $ED90

#org $ED79, $1ED89
    JMP $ED90 ; Cap checks for Laurels/Garlic. removed.
;;;;;;;;;;;;;;;;;;;;;;;
#org $8040, $C050
    JMP CheckRingForMarsh
;;;;;;;;;;;;;;;;;;;;;;;;
#org $8616, $4626
    JMP CheckWhiteCrystal_Horizontiblocks
;;;;;;;;;;;;;;;;;;;;;;;;;
#org $A8FE, $690E
    JMP CheckGoalConditions
;;;;;;;;;;;;;;;;;;;;;;;;
#org $C559, $1C569
    JMP LoadStartingHearts
;;;;;;;;;;;;;;;;;;;;;;;
#org $EFD2, $1EFE2
    JMP DisplayMerchantWhip
;;;;;;;;;;;;;;;;;;;;;;;
#org $C7E7, $1C7F7
    JMP OverrideNightColor

;This is my freespace code block
#org $B870, $3880
;;;;;;;;;;;;;;;;;;
;Death code. Triggers the GAME OVER screen when A + B + Start are pressed.
TriggerManualDeath:
    LDA $0026
    CMP #$01 ; Only process this if we're in the pause menu
    BNE .End
    LDA $F1
    AND #$D0
    CMP #$D0
    BNE .End
    LDA #$06
    STA $18 ; Trigger the Death screen while the menu is up

.End:
    JSR $C615
    RTS
;;;;;;;;;;;;;;;
;Redirect when dying, triggers on Menu not on death
LoadSaveMenu:
    LDA $26 ; Check if we were paused
    BEQ .Exit
    JSR $F403 ; Show sprites
    LDA #$00
    STA $26
    STA $6014 ; Crystal switch trigger
    JMP $C2AF ; Trigger game over
.Exit:
    JMP $C298


;;;;;;;;;;;;;;;;;;;
; Handles receiving an item from the server

GetItemFromServer:
    LDA $34
    BNE .DeathExit
    LDA $6010 ; Check if we've received an item currently
    BEQ .Exit
    JSR GetItemArbitrary
    LDA #$00
    STA $6010
.Exit:
    JMP $D778
.DeathExit:
    JMP $D79D
;;;;;;;;;;;;;;;;;;;;;;
; Receive any item complete with fanfare.
GetItemArbitrary:
!GetItemSub
.ClearAndExit:
    JSR $C118 ; Play sfx for the item
    RTS

;;;;;;;;;;;;;;;;;;
; Handles events when pressing A/B on the menu
ProcessExtraMenuInputs:
    LDA $F5
    AND #$20
    BNE .UnequipItem
    LDA $F5
    AND #$80
    BNE .SwapCrystalColor
    LDA $F5
    LSR A
    JMP $F2F9
.End:
    JMP $F2DF
.ExitNoSound:
    JMP $F307

; Normally there's no way to unequip anything, which can softlock if you only have the Heart...
.UnequipItem:
    TXA
    PHA

    LDX #$4F
    LDA $33 ; Menu row
    BEQ .Unequip
    LDX #$90
.Unequip:
    LDA #$00
    STA $00,X
    PLA
    TAX
    JMP .End
.SwapCrystalColor:
    LDA $33
    BNE .ExitNoSound ; We only want to run this if we're in the Relics section
    LDA $4F
    CMP #$06
    BNE .ExitNoSound ; This should only run if the Crystal is selected
.TryNextColor:
    LDA $6013
    CMP #$02
    BEQ .ResetCrystal
    CLC
    ADC #$01
.UpdateCrystalSprite:
    JSR CheckIfCrystalIsUnlocked
    CMP #$00
    BEQ .TryNextColor

    LDA #$00
    STA $7A
    INC $6014 ; Flag
    JMP .End
.ResetCrystal:
    LDA #$00
    BEQ .UpdateCrystalSprite

;;;;;;;;;;;;;;;;;
; Sets the Crystal's color based on CurSelectCrystal
CrystalSetColor:
    LDA $6013
    CLC
    ADC #$01
    JMP $F028
;;;;;;;;;;;;;;;;;;;;;;;;
; Reloads the row of Relics so we can refresh the crystal's sprite
ReloadCrystalGFX:
    LDA $6014
    BNE .Reload
    JSR $F0C4
    JMP $EFCB

.Reload:
    DEC $6014
    LDA $77
    CLC
    ADC #$08
    STA $77
    LDA $79
    CLC
    ADC #$08
    STA $79
    JSR $EE69
    JSR $EFEB
    LDA #$03
    STA $7A ; Set this so that the menu goes back to normal operation
    JMP $EFBC
;;;;;;;;;;;;;;;;;;;
; Check if Crystal A is unlocked
CrystalFlags:
    #byte $20, $40, $80

CheckIfCrystalIsUnlocked:
    STA $6013
    TAX
    LDA $91
    AND CrystalFlags,X
    BNE .CrystalActive
    LDA #$00
    RTS

.CrystalActive:
    LDA #$01
    RTS
;;;;;;;;;;;;;;;;;;;;
; Sets up APmem when starting a new game
InitializeNewGameData:
    JSR $C54B ; This initializes new game stuff including hearts. randomize later.
    LDX #$00
    LDA #$00
.Loop:
    STA $6010,X
    INX
    CPX #$30
    BNE .Loop
    LDX #$00
.BackupMemLoop:
    STA $6090,X
    INX
    CPX #$10
    BNE .BackupMemLoop
    RTS
;;;;;;;;;;;;;;;;;
; Loads new value for starting heart count
LoadStartingHearts:
    LDA $FF04
    STA $48
    LDA $FF05
    STA $49
    JMP $C55D



#org $9D30, $DD40
;Refill Garlic and Laurels when healing at the church
StockAtChurch:
    TXA
    PHA
    LDX #$00
    LDA $92
    AND #$01
    BEQ .SkipBag
    INX
.SkipBag:
    LDA $92
    AND #$04
    BEQ .SkipLaurels
    LDA #$04
    CPX #$00
    BEQ .LowLaurel
    CLC
    ADC #$04
.LowLaurel:
    STA $4C
.SkipLaurels:
    LDA $92
    AND #$08
    BEQ .Exit
    LDA #$04
    CPX #$00
    BEQ .LowGarlic
    CLC
    ADC #$04
.LowGarlic:
    STA $4D
.Exit:
    PLA
    TAX
    LDA $81
    STA $80
    JMP $EC9C
;;;;;;;;;;;;;;;;;;;;;



#org $B770, $7780
BitTable:
    #byte $01, $02, $04, $08, $10, $20, $40, $80

; Checks that the White Crystal is active
CheckBespokeCrystalWhite:
    LDA $4F
    CMP #$06 ; Make sure we have the Crystal equipped
    BNE .Disable 
    LDA $6013
    BNE .Disable ; Check this only if the Crystal Level is 1
    JMP $860B
.Disable:
    JMP $8604
;;;;;;;;;;;;;;;;;;;;
; Checks Blue crysyal
CheckBespokeCrystalBlue:
    LDA $6013
    CMP #$01 ; Blue Crystal
    BEQ .CrysActive
    JMP $A7B7
.CrysActive:
    JMP $A79B
;;;;;;;;;;;;;;;;;;;;
; Checcks red crystal
CheckBespokeCrystalRed:
    LDA $6013
    CMP #$02 ; Red Crystal
    BEQ .CrysActive
    JMP $A94B
.CrysActive:
    JMP $A944
;;;;;;;;;;;;;;;;;;;;;;;;;
; Checks Blue crysyal outside of mansion 4
CheckBespokeCrystalBlue_2:
    LDA $6013
    CMP #$01 ; Blue Crystal
    BEQ .CrysActive
    JMP $ADEC
.CrysActive:
    JMP $ADCA





; Records and stores the current Check ID, if necessary, when loading NPCS
check_pointer_list:
    #word $FFFF
    #word $9146, $90EB, $9141 ; Jova checks
    #word $9152, $914C, $9128 ; Alba checks
    #word $AF7B ; Graveyard duck
    #word $92B3, $92A7 ; Ondol checks
    #word $A888 ; Book near red crystal
    #word $9F9A, $9F8A, $9F9E ; Mansion 4
    #word $91FC ; Salesman in Doina
    #word $B2A4 ; Flame Whip guy
    #word $B277 ; Book outside M.4
    #word $9A94, $9A58, $9AB9, $9ABE ; Mansion 5
    #word $AF25 ; River knife guy
    #word $91F2, $916F, $91E7, $91E2; Aljiba checks
    #word $9C3A, $9C46, $9C42, $9C3E ;Mansion 2
    #word $A6C8, $A6A3 ;Aljiba outskirts
    #word $92A1, $929D, $9298;Veros
    #word $9B2B, $9B30, $9B38, $9B80, $9B8C; Mansion 1
    #word $A842 ; Diamond guy
    #word $9C53, $9CCC, $9C93, $9CD1, $9CD6; Mansion 3
check_pointer_end:

check_table_size = check_pointer_end - check_pointer_list


LogCheckID:
    INY
    LDA ($3D),Y
    PHA
    STX $6090
    STY $6091 ; Make backups of these
    LDX #$00
.Loop:
    LDY #$00
    STY $6092

    LDA $3D
    CLC
    ADC $6091 ; Add Y to it so we catually get THIS check
    PHA
    LDA #$00
    ADC $3E
    STA $6094
    PLA

    CMP check_pointer_list,X
    BNE .CheckByte2
    INC $6092
.CheckByte2:
    LDA $6094
    CMP check_pointer_list + 1, X
    BNE .CheckIfIsCheck
    INC $6092
.CheckIfIsCheck:
    LDA $6092
    CMP #$02 ; If this is 2, both bytes are equal meaning it's in the Check Registry
    BEQ .RegisterCheck
    CPX #check_table_size - 2 ; Check if we're at the end of this list
    BEQ .End
    TXA
    CLC
    ADC #$02
    TAX
    JMP .Loop


.End:
    LDX $6090
    LDY $6091
    PLA
    RTS

.RegisterCheck:
    TXA
    LSR ; Shift so we get the numeric ID
    LDX $6090
    STA $60A0,X
    INC $6095
    JMP .End
;;;;;;;;;;;;;;;;;;;;;;;
; Reads the check that we had stored during LogCheckID and saves it when talking to an NPC
StoreCurrentCheck:
    LDA $04D4,X
    ORA $08
    STA $40
    LDA $60A0,X
    STA $6093
    RTS
;;;;;;;;;;;;;;;;;;;;;
SetNPCTalkToCheck:
    LDA $6093
    JSR CheckIfCheckChecked_bank1
    CMP #$01
    BEQ .Skip
    JSR LoadtoSRAM
    JSR $7000
    RTS
.Skip:
    LDA #$15
    STA $7F
    RTS

SetBookCheck:
    TXA
    PHA
    LDA #$80
    STA $3F
    LDA $60A0,X
    STA $6093

    JSR LoadtoSRAM
    JSR $7000
    PLA
    TAX
    JMP $87A4


LoadtoSRAM:
    LDX #$00
.Loop:
    LDA DummyLoadCode,X
    STA $7000,X ; Move this code into SRAM
    INX
    CPX #(DummyLoadEnd - DummyLoadCode) + 1
    BNE .Loop
    RTS


;Copy of the check setting code. Moved to SRAM
SRAMBankSwitch = $7000 + (BankSwitch - DummyLoadCode)
DummyLoadCode:
    LDA #$03
    JSR SRAMBankSwitch

    LDA $6093
    JSR ActivateCheckFromID
    LDA $6093
    TAX
    LDA ItemsTable,X
    JSR GetLocalItem
    LDA #$01
    JSR SRAMBankSwitch
    RTS

BankSwitch:
  sta $E000
  lsr a
  sta $E000
  lsr a
  sta $E000
  lsr a
  sta $E000
  lsr a
  sta $E000
  rts
DummyLoadEnd:
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Sets up book checks. Despawns object if checked
HandleBookChecks:
    LDA #$00
    STA $6095
    JSR LogCheckID
    PHA
    LDA $6095
    BEQ .End
    LDA $60A0,X
    JSR CheckIfCheckChecked_bank1
    CMP #$00
    BEQ .End
    LDA #$FF
    STA $03B4,X
.End:
    PLA
    RTS
;;;;;;;;;;;;;;;;;;;;;;;;;;;;
CheckIfCheckChecked_bank1:
    !CheckIfCheckChecked
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Handles the Flame Whip guy
SetFlameWhipCheck:
    LDA $6093
    JSR CheckIfCheckChecked_bank1
    CMP #$01
    BEQ .CheckAlreadyDone
    JSR LoadtoSRAM
    JSR $7000
    LDA #$0E
    STA $7F
    RTS
.CheckAlreadyDone:
    LDA #$15
    STA $7F
    RTS
;;;;;;;;;;;;;;;;;;;;;;;;;;;
SetCrystalTraderCheck:
    LDA $6093
    JSR CheckIfCheckChecked_bank1
    CMP #$01
    BEQ .Skip
    JSR LoadtoSRAM
    JSR $7000
    JMP $907F
.Skip:
    LDA #$15
    JMP $9085
;;;;;;;;;;;;;;;;;;;;;;;;;
; Check for the Blue Crystal guy
CheckBlueCrystalTrader:
    LDA #$40
    BIT $91 ; Check for the Blue Crystal
    BEQ .NotOwned
    JMP SetCrystalTraderCheck
.NotOwned:
    LDA #$03
    JMP $9085
;;;;;;;;;;;;;;;;;;;;;;
; White crystal checker for other block types
CheckWhiteCrystal_Horizontiblocks:
    LDA OptionFlag_WhiteCrys
    BEQ .Enable
    LDA $4F
    CMP #$06 ; Make sure we have the Crystal equipped
    BNE .Disable 
    LDA $6013
    BNE .Disable ; Check this only if the Crystal Level is 1
.Enable:
    LDA $03C6,X
    AND #$DF
.WriteState:
    STA $03C6,X
    LDA $0456,X
    JMP $8619
.Disable:
    LDA $03C6,X
    ORA #$20
    JMP .WriteState
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Check's the player's Goal stuff
OrbFlags:
    #byte $27, $1D, $2D, $0D, $14

CheckGoalConditions:
    LDA $92
    AND #$02 ; Not a goal thing, just check Magic Cross
    BEQ .Locked
    LDY #$00
    STY $6090
.OrbLoop:
    LDA OrbFlags,Y
    JSR CheckIfCheckChecked_bank1
    CMP #$01
    BNE .SkipOrbInc
    INC $6090
.SkipOrbInc:
    INY
    CPY #$05
    BNE .OrbLoop
    LDA $6090
    CMP OptionFlag_OrbReq
    BCC .Locked ; If Orbs checked < Orbs required, lock the gate
    LDX #$00
    LDY #$00
.PartsLoop:
    LDA BitTable,X
    BIT $91
    BEQ .SkipPartInc
    INY
.SkipPartInc:
    INX
    CPX #$06
    BCC .PartsLoop
    CPY OptionFlag_PartsReq
    BCC .Locked
    JMP $A90C
.Locked:
    JMP $A911


;;;;;;;;;;;;;;;
#org $BB20, $13B30
; Saves the APMem region as a backup.
SaveIntoFile:
    INC $19
    JSR SaveFileStuff
    LDX #$00
.Loop:
    LDA $6010,X
    STA $6040,X
    CPX #$2F
    BEQ .End
    INX
    JMP .Loop
.End:
    RTS

; Saves some extra variables into the file
SaveFileStuff:
    LDX #$00
.Loop:
    LDA $48, X ; Heart count
    STA $6020,X
    CPX #$02
    BEQ .EndHeartSave
    INX
    JMP .Loop
.EndHeartSave:
    LDA $90
    STA $6022
    LDA $4F
    STA $6023

    RTS
;;;;;;;;;;;;;;;;;;;;
;Transers data back into APmem from the save file
LoadIntoFile:
    LDA #$03
    STA $04EF
    LDX #$00
.Loop:
    LDA $6040,X
    STA $6010,X
    CPX #$2F
    BEQ .End
    INX
    JMP .Loop
.End:
    LDX #$00
.HLoop:
    LDA $6020,X
    STA $48,X
    CPX #$02
    BEQ .EndHeartLoad
    INX
    JMP .HLoop

.EndHeartLoad:
    LDX #$00
    LDA #$00
.BackupMemLoop:
    STA $6090,X
    INX
    CPX #$10
    BNE .BackupMemLoop

    LDA $6022
    STA $90
    LDA $6023
    STA $4F
    RTS
;;;;;;;;;;;;;;;
#org $9DA0, $DDB0
; Flags merchant checks as complete
ItemsTable:
#byte $FF, $13, $25, $01
#pad ItemsTable + $4D, $00

StandardIcons:
    #byte $20 ; AP Item
    #byte $5B ; Whip Upgrade
    #byte $58 ; Laurels
    #byte $6D ; Garlic
    #byte $5C ; Bag
    #byte $5A ; Cross
SubItemIcons:
    #byte $54 ; Knife
    #byte $55 ; Silver Knife
    #byte $6F ; Gold Knife
    #byte $57 ; Holy Water
    #byte $70 ; Diamond
    #byte $69 ; Fire
    #byte $59 ; Stake
RelicItemIcons:
    #byte $4E ; Rib
    #byte $4F ; Heart
    #byte $50 ; Eye
    #byte $51 ; Nail
    #byte $52 ; Ring
    #byte $5E ; White Crystal
    #byte $6E ; Blue Crystal
    #byte $5F ; Red Crystal
IconPtrs:
    #word StandardIcons, SubItemIcons, RelicItemIcons

GetItemFromTable:
    LDA $6093
    TAX
    LDA ItemsTable,X
    RTS

SetMerchantCheck:
    LDA $6093
    JSR ActivateCheckFromID
    JSR GetItemFromTable
    JSR GetLocalItem
    JMP $EDF7
;;;;;;;;;;;;;;;;;;;;;
; Toggles a check's flag
BitTable_Bank2:
    #byte $01, $02, $04, $08, $10, $20, $40, $80

ActivateCheckFromID:
    PHA
    TAY
    LDX #$00
.Loop:
    CPY #$08
    BCC .ExitLoop
    TYA
    SEC
    SBC #$08
    TAY
    INX
    JMP .Loop
.ExitLoop:
    LDA BitTable_Bank2,Y
    STA $6024
    LDA $6030,X
    ORA $6024
    STA $6030,X
    PLA
    RTS
;;;;;;;;;;;;;;;;;;;
; Instead of loading the actual icon for this dialogue, instead reference the placed item ID
LoadItemIcon:
    STX $6091
    JSR GetItemFromTable
    BIT BitTable_Bank2 + 7
    BNE .LoadHeartIcon

    PHA
    LSR
    LSR
    LSR
    TAX
    LDA IconPtrs,X
    STA $F1
    LDA IconPtrs + 1,X
    STA $F2
    PLA
    AND #$0F
    STY $6090
    TAY
    LDA ($F1),Y
    LDY $6090
    LDX $6091
    JMP $ECE7
.LoadHeartIcon:
    LDX $6091
    LDA #$61
    JMP $ECE7

; Gets an item, but called in another bank. Also doesn't play any sound
GetLocalItem:
    !GetItemSub
    .ClearAndExit:
        RTS
;;;;;;;;;;;;;;;;;;;;;;
BlueCrystalTradeText:
;Text ID 0x03
;SHOW ME A BLUE CRYSTAL. I'LL MAKE IT WORTH YOUR WHILE.
#byte $13, $08, $0F, $17, $00, $0D, $05, $00, $01, $FE
#byte $02, $0C, $15, $05, $00, $03, $12, $19, $13, $14, $01, $0C, $1B, $FE
#byte $09, $1C, $0C, $0C, $00, $0D, $01, $0B, $05, $00, $09, $14, $FE
#byte $17, $0F, $12, $14, $08, $00, $19, $0F, $15, $12, $FE
#byte $17, $08, $09, $0C, $05, $1B, $FF
WhiteCrystalTradeText:
;Text ID 0x6B
;I'LL TRADE SOMETHING GOOD FOR A WHITE CRYSTAL.
#byte $09, $1C, $0C, $0C, $00, $14, $12, $01, $04, $05, $FE
#byte $13, $0F, $0D, $05, $14, $08, $09, $0E, $07, $FE
#byte $07, $0F, $0F, $04, $00, $06, $0F, $12, $00, $01, $FE
#byte $17, $08, $09, $14, $05, $FE
#byte $03, $12, $19, $13, $14, $01, $0C, $1B, $FF
CheckCompletedText:
;GO AWAY, I HAVE NOTHING TO GIVE TO YOU.
#byte $07, $0F, $00, $01, $17, $01, $19, $1E, $00, $09, $FE
#byte $08, $01, $16, $05, $00, $0E, $0F, $14, $08, $09, $0E, $07, $FE
#byte $14, $0F, $00, $07, $09, $16, $05, $00, $14, $0F, $FE
#byte $14, $08, $05, $00, $0C, $09, $0B, $05, $13, $00, $0F, $06, $FE
#byte $19, $0F, $15, $1B, $FF
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Tex_APItem:
;AN AP ITEM
#byte $01, $0E, $00, $01, $10, $FE, $09, $14, $05, $0D, $FF
Tex_Laurels:
;SOME LAURELS
#byte $13, $0F, $0D, $05, $FE, $0C, $01, $15, $12, $05, $0C, $13, $FF
Tex_Garlic:
;SOME GARLIC
#byte $13, $0F, $0D, $05, $FE, $07, $01, $12, $0C, $09, $03, $FF
Tex_Bag:
;A SILK BAG
#byte $01, $00, $13, $09, $0C, $0B, $FE, $02, $01, $07, $FF
Tex_Cross:
;THE MAGIC CROSS
#byte $14, $08, $05, $00, $0D, $01, $07, $09, $03, $FE
#byte $03, $12, $0F, $13, $13, $FF
Tex_Knife:
;A DAGGER
#byte $01, $00, $04, $01, $07, $07, $05, $12, $FF
Tex_SKnife:
;A SILVER KNIFE
#byte $01, $00, $13, $09, $0C, $16, $05, $12, $FE
#byte $0B, $0E, $09, $06, $05, $FF
Tex_GKnife:
;A GOLDEN KNIFE
#byte $01, $00, $07, $0F, $0C, $04, $05, $0E, $FE
#byte $0B, $0E, $09, $06, $05, $FF
Tex_Water:
;HOLY WATER
#byte $08, $0F, $0C, $19, $FE, $17, $01, $14, $05, $12, $FF
Tex_Dmnd:
;A DIAMOND
#byte $01, $FE, $04, $09, $01, $0D, $0F, $0E, $04, $FF
Tex_Fire:
;THE SACRED FLAME
#byte $14, $08, $05, $FE, $13, $01, $03, $12, $05, $04, $00
#byte $06, $0C, $01, $0D, $05, $FF
Tex_Stake:
;AN OAK STAKE
#byte $01, $0E, $00, $0F, $01, $0B, $FE, $13, $14, $01, $0B, $05, $FF
Tex_Rib:
;Dracula's Rib
#byte $04, $12, $01, $03, $15, $0C, $01, $1C, $13, $FE
#byte $12, $09, $02, $FF
Tex_DracHeart:
;Dracula's Heart
#byte $04, $12, $01, $03, $15, $0C, $01, $1C, $13, $FE
#byte $08, $05, $01, $12, $14, $FF
Tex_Eye:
;Dracula's Eyeball
#byte $04, $12, $01, $03, $15, $0C, $01, $1C, $13, $FE
#byte $05, $19, $05, $02, $01, $0C, $0C, $FF
Tex_Nail:
;DRACULA'S NAIL
#byte $04, $12, $01, $03, $15, $0C, $01, $1C, $13, $FE
#byte $0E, $01, $09, $0C, $FF
Tex_Ring:
;DRACULA'S RING
#byte $04, $12, $01, $03, $15, $0C, $01, $1C, $13, $FE
#byte $12, $09, $0E, $07, $FF
Tex_WCrys:
;A WHITE CRYSTAL
#byte $01, $00, $17, $08, $09, $14, $05, $FE
#byte $03, $12, $19, $13, $14, $01, $0C, $FF
Tex_BCrys:
;A BLUE CRYSTAL
#byte $01, $00, $02, $0C, $15, $05, $FE
#byte $03, $12, $19, $13, $14, $01, $0C, $FF
Tex_RCrys:
;A RED CRYSTAL
#byte $01, $00, $12, $05, $04, $FE
#byte $03, $12, $19, $13, $14, $01, $0C, $FF
Tex_FillerHearts:
;SOME HEARTS
#byte $13, $0F, $0D, $05, $FE, $08, $05, $01, $12, $14, $13, $FF
Tex_ThornWhip:
;THE THORN WHIP
#byte $14, $08, $05, $00, $14, $08, $0F, $12, $0E, $FE
#byte $17, $08, $09, $10, $FF
Tex_ChainWhip:
;THE CHAIN WHIP
#byte $14, $08, $05, $00, $03, $08, $01, $09, $0E, $FE
#byte $17, $08, $09, $10, $FF
Tex_MorningStar:
;THE MORNING STAR
#byte $14, $08, $05, $00, $0D, $0F, $12, $0E, $09, $0E, $07, $FE
#byte $13, $14, $01, $12, $FF
Tex_FlameWhip:
;THE FLAME WHIP
#byte $14, $08, $05, $00, $06, $0C, $01, $0D, $05, $FE
#byte $17, $08, $09, $10, $FF


;;;;;;;;;;;;;;;;;;
; By a miracle of programming, Text ID $6B is hardcoded to not play sound.
; Expand that.
SetNothingSounds:
    LDA $7F
    CMP #$6B
    BEQ .None
    CMP #$15
    BEQ .None
    CMP #$03
    BEQ .None
    JMP $EF10
.None:
    JMP $EF15
;;;;;;;;;;;;;;;;;;;;;;;;;;
; Check if we're printing char FA. If we are, redirect into dynamic item names.
ItemNamePointers:
#word Tex_APItem, Tex_FillerHearts, Tex_Laurels, Tex_Garlic, Tex_Bag, Tex_Cross
SubNames:
#word Tex_Knife, Tex_SKnife, Tex_GKnife, Tex_Water, Tex_Dmnd, Tex_Fire, Tex_Stake
RelNames:
#word Tex_Rib, Tex_DracHeart, Tex_Eye, Tex_Nail, Tex_Ring, Tex_WCrys, Tex_BCrys, Tex_RCrys
WhipNames:
#word Tex_ThornWhip, Tex_ChainWhip, Tex_MorningStar, Tex_FlameWhip, Tex_FlameWhip ; Extra in case we're already AT flame whip

PtrTypes:
#word ItemNamePointers, SubNames, RelNames, WhipNames

GetDynamicItemName:
    CMP #$FF ; Check if it's a terminator
    BEQ .Terminator
    CMP #$F9
    BEQ .Skip

    CMP #$FA
    BNE .End
    LDA $7C
    STA $6099
    LDA $7F
    STA $6096

    LDA #$FF
    STA $7F

    JSR GetItemFromTable
    CMP #$01
    BEQ .GetProgressiveWhipName
    BIT BitTable_Bank2 + 7
    BNE .GetHearts
.LoadFromTable:
    PHA
    LDY #$00
    STY $7C
    STY $609C
    LSR
    LSR
    LSR
    TAX
    LDA PtrTypes,X
    STA $F1
    LDA PtrTypes + 1,X
    STA $F2
    PLA
    AND #$0F
    ASL
    TAY

    LDA ($F1),Y
    STA $6097
    INY
    LDA ($F1),Y
    STA $6098
    JMP $EE9D

.Terminator:
    LDA $7F
    CMP #$FF
    BNE .EndTex
    LDA $6096
    STA $7F

    LDA $6099
    STA $7C
    JMP $EE9D

.EndTex:
    JMP $EF03
.End:
    JMP $EEBC
.GetHearts:
    LDA #$01 ; Filler hearts
    JMP .LoadFromTable
.GetProgressiveWhipName:
    LDA $434 ;Current whip level is table index
    PHA
    LDA $609C
    BNE .LoadMerchantWhip
    PLA
    SEC
    SBC #$01
    JMP .LoadItemWhip

.LoadMerchantWhip:
    PLA
.LoadItemWhip:
    CLC
    ADC #$30
    JMP .LoadFromTable
.Skip:
    JMP $EEB2
;;;;;;;;;;;;;;;;;;
GetDynaTexPointr:
    LDA $7F
    CMP #$FF
    BNE .Exit
    LDA $6097
    STA $00
    LDA $6098
    STA $01
    JMP $EEB2
.Exit:
    ASL
    JMP $EEA7
;;;;;;;;;;;;;;;;;;;;;
;Prevents merchant checks from being done again
MerchantNonRenewableCheck:
LDA $6093
JSR CheckIfCheckChecked_bank2
CMP #$01
BEQ .Skip
LDA $28
LDY $29
JMP $ED94
;;;;;;;;;;;;;;;;;;
.Skip:
    JMP $EDFE

CheckIfCheckChecked_bank2:
    !CheckIfCheckChecked
    RTS
;;;;;;;;;;;;;;;;;;;;
; If enabled, stops Swamp damage if you have the ring equipped
CheckRingForMarsh:
    LDA OptionFlag_MarshProt
    CMP #$01
    BNE .ExitNormal
    LDA $4F
    CMP #$05 ; Check if the Ring is equipped
    BNE .ExitNormal
    JMP $8030 ; If the ring is equipped, skip the damage routine outright


.ExitNormal:
    LDA #$00
    JSR $D3AC
    JMP $8043
;;;;;;;;;;;;;;;;;;;;;;
; Sets a variable for whip name display during Merchant checks
DisplayMerchantWhip:
    INC $609C
    LDY #$02
    JMP $EFD8
;;;;;;;;;;;;;;;;;;;;
#org $BF00, $BF10
; Ignores the night color setting if in a house
OverrideNightColor:
    LDA $8F
    BNE .DayColor
    LDA $82
    BEQ .DayColor
    JMP $C7EB
.DayColor:
    JMP $C7ED



#IncSrc "apc2_tex_ptrs.asm"
#IncSRC "apc2_option_flags.asm"
