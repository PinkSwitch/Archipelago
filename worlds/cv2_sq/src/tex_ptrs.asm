#org $8B88, $CB98
    #word BlueCrystalTradeText

#org $8BAC, $CBBC
    #word CheckCompletedText

#org $8C58, $CC68
    #word WhiteCrystalTradeText

#org $8E79, $CE89
    ; Morning star check, ID = E
    #byte $09, $1C, $0C, $0C, $00, $07, $09, $16, $05, $00, $19, $0F, $15, $FE
    #byte $FA, $1B, $FF

#org $8EBC, $CECC
    ; Silk bag check
    #byte $FA, $1B, $FF

#org $8ED6, $CEE6
    ; Silver knife
    #byte $FA, $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9, $F9

#org $8B9C, $CBAC
    ; Book 1
    #word $9C8E

#org $8BA4, $CBB4
    ; book 13
    #word $9C8E

#org $8F36, $CF46
    #byte $FA, $1B, $FF

#org $8BAA, $CBBA
    ; Book 11
    #word $9C8E

#org $8F9D, $CFAD
    ; Drac Rib
    #byte $FA, $1B, $FF

#org $8FBD, $CFCD
    ; Drac Heart
    #byte $FA, $1B, $FF

#org $8FDF, $CFEF
    ; Drac Eye
    #byte $FA, $1B, $FF

#org $9003, $D013
    ; Drac Nail
    #byte $FA, $1B, $FF

#org $9024, $D034
    ; Drac Ring
    #byte $FA, $1B, $FF
;;;;;;;;;;;;;;;;;;;;;;
;Oak text
#org $8BBC, $CBCC
    #word $904C

#org $8BBE, $CBCE
    ;Book 2 | Book 3 | Book 4 | Book 8 | Book 7 | Book 9 | Book 10 | Book 12 |M. Cross|
    #word $9C8E, $9C8E, $9C8E, $9C8E, $9C8E, $9C8E, $9C8E, $9C8E, $9C8E
;;;;;;;;;;;;;;;;;;;;;;;
#org $91D7, $D1E7
    #byte $FA, $1B, $FF

#org $9C9E, $DCAE
    #byte $FA, $1B, $FF

#org $9CE7, $DCF7
    #byte $FA, $1B, $FF

#org $9CC0, $DCD0
    #byte $FA, $1B, $FF
;;;;;;;;;;;;;;;;;;;;;;
#org $8BE2, $CBF2
    #word $91F1, $91F1
    
#org $8BE6, $CBF6
    #word $91F1, $91F1, $91F1, $91F1, $91F1, $91F1

#org $91F1, $D201
    #byte $02, $15, $19, $00, $FA, $5D, $FF

    ;#word $8BBE