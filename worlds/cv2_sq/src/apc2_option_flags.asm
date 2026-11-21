#org $BE00, $FE10
    OptionFlag_MarshProt: ; be00
    #byte $00

#org $FF01, $1FF11
    OptionFlag_WhiteCrys:
    #byte $00
    OptionFlag_OrbReq:
    #byte $00 ;1FF12
    OptionFlag_PartsReq:
    #byte $05 ;1FF13
StartingHearts:
    #byte $50, $00