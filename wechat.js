var n = {}
function d(e, t) {
var n = (65535 & e) + (65535 & t);
return (e >> 16) + (t >> 16) + (n >> 16) << 16 | 65535 & n
}
function s(e, t, n, o, i, r) {
return d((a = d(d(t, e), d(o, r))) << (s = i) | a >>> 32 - s, n);
var a, s
}
function p(e, t, n, o, i, r, a) {
return s(t & n | ~t & o, e, t, i, r, a)
}
function f(e, t, n, o, i, r, a) {
return s(t & o | n & ~o, e, t, i, r, a)
}
function m(e, t, n, o, i, r, a) {
return s(t ^ n ^ o, e, t, i, r, a)
}
function h(e, t, n, o, i, r, a) {
return s(n ^ (t | ~o), e, t, i, r, a)
}
function c(e, t) {
e[t >> 5] |= 128 << t % 32,
e[14 + (t + 64 >>> 9 << 4)] = t;
var n, o, i, r, a, s = 1732584193,
c = -271733879,
u = -1732584194,
l = 271733878;
for (n = 0; n < e.length; n += 16) s = p(o = s, i = c, r = u, a = l, e[n], 7, -680876936),
l = p(l, s, c, u, e[n + 1], 12, -389564586),
u = p(u, l, s, c, e[n + 2], 17, 606105819),
c = p(c, u, l, s, e[n + 3], 22, -1044525330),
s = p(s, c, u, l, e[n + 4], 7, -176418897),
l = p(l, s, c, u, e[n + 5], 12, 1200080426),
u = p(u, l, s, c, e[n + 6], 17, -1473231341),
c = p(c, u, l, s, e[n + 7], 22, -45705983),
s = p(s, c, u, l, e[n + 8], 7, 1770035416),
l = p(l, s, c, u, e[n + 9], 12, -1958414417),
u = p(u, l, s, c, e[n + 10], 17, -42063),
c = p(c, u, l, s, e[n + 11], 22, -1990404162),
s = p(s, c, u, l, e[n + 12], 7, 1804603682),
l = p(l, s, c, u, e[n + 13], 12, -40341101),
u = p(u, l, s, c, e[n + 14], 17, -1502002290),
s = f(s, c = p(c, u, l, s, e[n + 15], 22, 1236535329), u, l, e[n + 1], 5, -165796510),
l = f(l, s, c, u, e[n + 6], 9, -1069501632),
u = f(u, l, s, c, e[n + 11], 14, 643717713),
c = f(c, u, l, s, e[n], 20, -373897302),
s = f(s, c, u, l, e[n + 5], 5, -701558691),
l = f(l, s, c, u, e[n + 10], 9, 38016083),
u = f(u, l, s, c, e[n + 15], 14, -660478335),
c = f(c, u, l, s, e[n + 4], 20, -405537848),
s = f(s, c, u, l, e[n + 9], 5, 568446438),
l = f(l, s, c, u, e[n + 14], 9, -1019803690),
u = f(u, l, s, c, e[n + 3], 14, -187363961),
c = f(c, u, l, s, e[n + 8], 20, 1163531501),
s = f(s, c, u, l, e[n + 13], 5, -1444681467),
l = f(l, s, c, u, e[n + 2], 9, -51403784),
u = f(u, l, s, c, e[n + 7], 14, 1735328473),
s = m(s, c = f(c, u, l, s, e[n + 12], 20, -1926607734), u, l, e[n + 5], 4, -378558),
l = m(l, s, c, u, e[n + 8], 11, -2022574463),
u = m(u, l, s, c, e[n + 11], 16, 1839030562),
c = m(c, u, l, s, e[n + 14], 23, -35309556),
s = m(s, c, u, l, e[n + 1], 4, -1530992060),
l = m(l, s, c, u, e[n + 4], 11, 1272893353),
u = m(u, l, s, c, e[n + 7], 16, -155497632),
c = m(c, u, l, s, e[n + 10], 23, -1094730640),
s = m(s, c, u, l, e[n + 13], 4, 681279174),
l = m(l, s, c, u, e[n], 11, -358537222),
u = m(u, l, s, c, e[n + 3], 16, -722521979),
c = m(c, u, l, s, e[n + 6], 23, 76029189),
s = m(s, c, u, l, e[n + 9], 4, -640364487),
l = m(l, s, c, u, e[n + 12], 11, -421815835),
u = m(u, l, s, c, e[n + 15], 16, 530742520),
s = h(s, c = m(c, u, l, s, e[n + 2], 23, -995338651), u, l, e[n], 6, -198630844),
l = h(l, s, c, u, e[n + 7], 10, 1126891415),
u = h(u, l, s, c, e[n + 14], 15, -1416354905),
c = h(c, u, l, s, e[n + 5], 21, -57434055),
s = h(s, c, u, l, e[n + 12], 6, 1700485571),
l = h(l, s, c, u, e[n + 3], 10, -1894986606),
u = h(u, l, s, c, e[n + 10], 15, -1051523),
c = h(c, u, l, s, e[n + 1], 21, -2054922799),
s = h(s, c, u, l, e[n + 8], 6, 1873313359),
l = h(l, s, c, u, e[n + 15], 10, -30611744),
u = h(u, l, s, c, e[n + 6], 15, -1560198380),
c = h(c, u, l, s, e[n + 13], 21, 1309151649),
s = h(s, c, u, l, e[n + 4], 6, -145523070),
l = h(l, s, c, u, e[n + 11], 10, -1120210379),
u = h(u, l, s, c, e[n + 2], 15, 718787259),
c = h(c, u, l, s, e[n + 9], 21, -343485551),
s = d(s, o),
c = d(c, i),
u = d(u, r),
l = d(l, a);
return [s, c, u, l]
}
function u(e) {
var t, n = "";
for (t = 0; t < 32 * e.length; t += 8) n += String.fromCharCode(e[t >> 5] >>> t % 32 & 255);
return n
}
function l(e) {
var t, n = [];
for (n[(e.length >> 2) - 1] = void 0, t = 0; t < n.length; t += 1) n[t] = 0;
for (t = 0; t < 8 * e.length; t += 8) n[t >> 5] |= (255 & e.charCodeAt(t / 8)) << t % 32;
return n
}
function o(e) {
var t, n, o = "0123456789abcdef",
i = "";
for (n = 0; n < e.length; n += 1) t = e.charCodeAt(n),
i += o.charAt(t >>> 4 & 15) + o.charAt(15 & t);
return i
}
function i(e) {
return unescape(encodeURIComponent(e))
}
function r(e) {
return u(c(l(t = i(e)), 8 * t.length));
var t
}
function a(e, t) {
return function(e, t) {
    var n, o, i = l(e),
    r = [],
    a = [];
    for (r[15] = a[15] = void 0, 16 < i.length && (i = c(i, 8 * e.length)), n = 0; n < 16; n += 1) r[n] = 909522486 ^ i[n],
    a[n] = 1549556828 ^ i[n];
    return o = c(r.concat(l(t)), 512 + 8 * t.length),
    u(c(a.concat(o), 640))
} (i(e), i(t))
}
function getPwd(e, t, n) {
return t ? n ? a(t, e) : o(a(t, e)) : n ? r(e) : o(r(e))
}