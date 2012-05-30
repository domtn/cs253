UNIT 3

ACID

Atomicity - all parts of a transaction succeed or fail together
            (group of multiple commands)

Consistency - the database will always be consistent

 E.g.: 
    User    Link
    ----    ----
    karma   score
    
    karma and score must be updated at the same time



Isolation - no transcation can interfere with another


Durability - once the transaction is committed, it won't be lost