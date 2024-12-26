parent_traits = {
    "Life": {
        1: ["Secret Herb"],
        3: ["Horn of Life", "Cup of Lifenoodles"]
    },

    "Doll": {
        1: ["Teddy Bear"],
        3: ["Super Plush Bear"]
    },
    
    "Food": {},
}

# What should happen; If there are multiple traits in this table, we use the one with the highest quality.
# If multiple have the same quality, prioritize whichever one was first.