#macro GetItemSub
    STA $31
    BIT .BitTable + 7
    BNE .GetItemHearts
    CMP #$00
    BEQ .GetItemAP

    CMP #$01
    BEQ .GetItemWhipUpgrade
    CMP #$02
    BEQ .GetItemLaurels
    CMP #$03
    BEQ .GetItemGarlic
    CMP #$10
    BCC .GiveRelics2
    PHA
    AND #$10
    BNE .GetItemSubweapon
    PLA
    PHA
    AND #$20
    BNE .GetItemRelic
    PLA

.GetItemAP:
    JMP .ClearAndExit
.GetItemHearts:
    JMP .AddHearts
.GetItemWhipUpgrade:
    LDA $434
    CMP #$04
    BCS .SkipWhip
    INC $434
.SkipWhip:
    LDA #$20
    JMP .ClearAndExit
;;;;;;;;;;;;;;;;;;;;
.GetItemSubweapon:
    PLA
    TAX
    PHA
    LDA $31
    SEC
    SBC #$10
    TAX
    LDA $4A
    ORA .BitTable,X
    STA $4A
    PLA
    TAX
    LDA #$22
    JMP .ClearAndExit
.GetItemRelic:
    PLA
    JMP .GiveRelic
.GetItemLaurels:
    LDA $92
    ORA #$04 ; Set the Laurels Owned bit
    STA $92
    AND #$01 ; Check for Silk Bag
    BNE .LHasBag
    LDA #$04
    JMP .LNoBag
.LHasBag:
    LDA #$08
.LNoBag:
    STA $4C
    LDA #$1F
    JMP .ClearAndExit
.GetItemGarlic:
    LDA $92
    ORA #$08
    STA $92
    AND #$01
    BNE .GHasBag
    LDA #$04
    JMP .GNoBag
.GHasBag:
    LDA #$08
.GNoBag:
    STA $4D
    LDA #$1F
    JMP .ClearAndExit
.GiveRelics2:
    TXA
    PHA
    LDX #$01
    LDA $31
    CMP #$05
    BNE .GiveBag
    LDX #$02
.GiveBag:
    STX $31
    LDA $92
    ORA $31
    STA $92
    PLA
    TAX
    LDA #$22
    JMP .ClearAndExit

.GiveRelic:
    TXA
    PHA
    LDA $31
    SEC
    SBC #$20
    PHA
    LDX #$00
    TAX
    LDA $91
    ORA .BitTable,X
    STA $91
    PLA
    CMP #$05
    BCC .EndRelic
    SEC
    SBC #$05 
    STA $6013 ; Update the current CrystalLevel
.EndRelic:
    PLA
    TAX
    LDA #$22
    JMP .ClearAndExit
.AddHearts:
    AND #$7F
    STA $08
    LDA $48
    STA $09
    JSR $DEDE
    STA $48
    BCC .HSkip
    LDA #$01
    STA $08
    LDA $49
    STA $09
    JSR $DEDE
    STA $49
.HSkip:
    LDA #$1F
    JMP .ClearAndExit

.BitTable:
    #byte $01, $02, $04, $08, $10, $20, $40, $80
#endmacro
;;;;;;;;;;;;;;;;;;;
#macro CheckIfCheckChecked

.CheckIfChecked:
    STX $6090
    STY $6091
    LDX #$00
.Loop:
    CMP #$08
    BCC .Done
    INX
    SEC
    SBC #$08
    JMP .Loop
.Done:
    TAY
    LDA .BitTable,Y
    STA $6094
    LDA $6030,X
    BIT $6094
    BNE .CheckIsSet
    LDA #$00
.Exit:
    LDX $6090
    LDY $6091
    RTS
.CheckIsSet:
    LDA #$01
    BNE .Exit

.BitTable:
    #byte $01, $02, $04, $08, $10, $20, $40, $80
#endmacro