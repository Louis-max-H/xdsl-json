typedef struct foo {
struct {
    long field1;
    struct {
    long field2;
    long field3;
    union {
        long field4;
        char field5[32];
    } quux;
    long field6;
    long field7;
    } baz;
    long field8;
} bar;
} foo;

foo chunky;

char take_field(void) {
    return chunky.bar.baz.quux.field5[17];
}
