test('sum is ok', () => {
    expect(1).toBe(2);
});




const { login } = require('./util');

test('je moet een warning message krijgen', () => {
    const test = login(' ', ' ');
    expect(test).toBe(' ');
});