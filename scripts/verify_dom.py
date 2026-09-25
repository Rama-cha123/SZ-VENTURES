from html.parser import HTMLParser
import sys

files = ['index.html', 'ventures/index.html', 'portfolio.html', 'new-economy.html', 'new-economy/index.html']

class DOMNode:
    def __init__(self, tag, attrs, parent=None):
        self.tag = tag
        self.attrs = dict(attrs)
        self.parent = parent
        self.children = []

    def get_class(self):
        return self.attrs.get('class', '')

    def get_id(self):
        return self.attrs.get('id', '')

    def get_href(self):
        return self.attrs.get('href', '')

    def ancestors(self):
        curr = self.parent
        res = []
        while curr:
            res.append(curr)
            curr = curr.parent
        return res

class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = DOMNode('root', {})
        self.current = self.root
        self.all_nodes = []
        # Void elements in HTML
        self.void_tags = {'meta', 'link', 'img', 'br', 'hr', 'input', 'source', 'path', 'svg', 'circle', 'polyline', 'polygon', 'rect', 'wbr'}

    def handle_starttag(self, tag, attrs):
        node = DOMNode(tag, attrs, self.current)
        self.current.children.append(node)
        self.all_nodes.append(node)
        if tag.lower() not in self.void_tags:
            self.current = node

    def handle_endtag(self, tag):
        if tag.lower() in self.void_tags:
            return
        curr = self.current
        while curr and curr.tag.lower() != tag.lower():
            curr = curr.parent
        if curr and curr.parent:
            self.current = curr.parent

print("==================== PROGRAMMATIC DOM VALIDATION ====================")
all_checks_passed = True

for fpath in files:
    print(f"\n--- Checking {fpath} ---")
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    parser = TreeBuilder()
    parser.feed(html)

    # Find SnapOps card
    snapops_cards = []
    ch_cards = []

    for node in parser.all_nodes:
        if node.tag == 'a':
            href = node.get_href()
            cls = node.get_class()
            if '/snapops/' in href and ('company' in cls or 'venture-card' in cls):
                snapops_cards.append(node)
            if '/creator-house/' in href and ('company' in cls or 'venture-card' in cls):
                ch_cards.append(node)

    print(f"SnapOps venture cards found: {len(snapops_cards)}")
    print(f"Creator House venture cards found: {len(ch_cards)}")

    if len(snapops_cards) != 1:
        print(f"FAIL: Expected exactly 1 SnapOps card, found {len(snapops_cards)}")
        all_checks_passed = False
        continue

    card = snapops_cards[0]
    ch_card = ch_cards[0] if ch_cards else None

    # Ancestor checks
    ancestors = card.ancestors()
    ancestor_tags = [a.tag for a in ancestors]
    ancestor_classes = [a.get_class() for a in ancestors]
    ancestor_ids = [a.get_id() for a in ancestors]

    # Check 1: not descendant of header
    in_header = 'header' in ancestor_tags
    print(f"1. Is descendant of <header>: {in_header} ({'PASS' if not in_header else 'FAIL'})")
    if in_header: all_checks_passed = False

    # Check 2: not descendant of nav
    in_nav = 'nav' in ancestor_tags
    print(f"2. Is descendant of <nav>: {in_nav} ({'PASS' if not in_nav else 'FAIL'})")
    if in_nav: all_checks_passed = False

    # Check 3: not inside .nav__inner, .nav__links, .nav__right, or mobile menu
    nav_inner_check = any('nav__inner' in c for c in ancestor_classes)
    nav_links_check = any('nav__links' in c for c in ancestor_classes)
    nav_right_check = any('nav__right' in c for c in ancestor_classes)
    menu_check = any('menu' in c for c in ancestor_classes) or any('menu' in i for i in ancestor_ids)
    in_nav_components = nav_inner_check or nav_links_check or nav_right_check or menu_check
    print(f"3. Inside nav components/menu: {in_nav_components} ({'PASS' if not in_nav_components else 'FAIL'})")
    if in_nav_components: all_checks_passed = False

    # Check 4: immediate parent
    parent = card.parent
    parent_tag = parent.tag if parent else 'None'
    parent_cls = parent.get_class() if parent else ''
    print(f"4. Immediate parent: <{parent_tag} class=\"{parent_cls}\">")

    # Check 5: same parent as Creator House
    same_parent = (ch_card is not None) and (ch_card.parent == card.parent)
    print(f"5. Shares immediate parent with Creator House: {same_parent} ({'PASS' if same_parent else 'FAIL'})")
    if not same_parent: all_checks_passed = False

    # Check 6: follows Creator House card
    if same_parent:
        parent_children = parent.children
        ch_idx = parent_children.index(ch_card)
        snap_idx = parent_children.index(card)
        follows_ch = (snap_idx == ch_idx + 1)
        print(f"6. Immediately follows Creator House card (index {ch_idx} -> {snap_idx}): {follows_ch} ({'PASS' if follows_ch else 'FAIL'})")
        if not follows_ch: all_checks_passed = False

print(f"\nOverall DOM Validation Result: {'ALL CHECKS PASSED' if all_checks_passed else 'SOME CHECKS FAILED'}")
