# Folkdance
An implementation of common player/entity interactions for Driftwood 2D.

This Driftwood 2D library will provide solid default implementations for entity AI, entity-entity and player-entity interactions,  combat, items, inventory, and other things the player and entities need to interact with each other and the world in meaningful ways. Folkdance can be thought of as a sub-engine.

Because so much variation is possible, I felt it would be better to make this a separate package rather than part of the standard library. The Driftwood 2D standard library should be reserved for useful code snippets that probably only ever need to be implemented once.

It is also likely that if this were to remain part of the main Driftwood repository, it would eventually make up the vast majority of entries in the issue tracker. Splitting it into another repository promotes cleanliness and encapsulation.
