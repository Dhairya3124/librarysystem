from flask import render_template,flash,redirect
from app.forms import BookForm,MemberForm,ImportForm,IssueForm,SearchForm, ReturnForm
import sqlite3
from datetime import datetime
from app import app
import sys
import requests

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    
    return render_template('index.html', title='Home', user=user)

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/search',methods = ["POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search.data
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row
        cur = connection.cursor()
        # result = 
        books = cur.execute("SELECT * FROM books WHERE title LIKE '%"+search+"%'").fetchall()
        cur.close()
        if len(books) > 0:
            return render_template('books.html', books=books)
        else:
            msg = 'No Books Found'
            return render_template('books.html', books=books, msg=msg)




@app.route('/books',methods = ["GET","POST"])
def books():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    # result = 
    books = cur.execute("SELECT * FROM books").fetchall()
    cur.close()

    # Render Template
    if len(books) > 0:
        return render_template('books.html', books=books)
    else:
        msg = 'No Books Found'
        return render_template('books.html', books=books, msg=msg)
@app.route('/book/<string:id>',methods = ["GET","POST"])
def book(id):
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    # result = 
    book = cur.execute("SELECT * FROM books WHERE bookID = '"+id+"'").fetchone()
    cur.close()
    if book:
        return render_template('book_detail.html', book=book)
    else:
        msg = 'No Book Found'
        return render_template('book_detail.html', book=book, msg=msg)
@app.route('/addbooks',methods = ["GET","POST"])
def addbook():
    form = BookForm()
    if form.validate_on_submit():
        bookID = form.bookID.data
        title = form.title.data
        authors = form.authors.data
        average_rating = form.average_rating.data
        isbn = form.isbn.data
        isbn13 = form.isbn13.data
        language_code = form.language_code.data
        num_pages = form.num_pages.data
        ratings_count = form.ratings_count.data
        text_reviews_count = form.text_reviews_count.data
        publication_date = form.publication_date.data
        publisher = form.publisher.data
        total_count = form.total_count.data
        available_count = form.total_count.data
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO books (bookID,title,authors,average_rating,isbn,isbn13,language_code,num_pages,ratings_count,text_reviews_count,publication_date,publisher,total_count,available_count) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(bookID,title,authors,average_rating,isbn,isbn13,language_code,num_pages,ratings_count,text_reviews_count,publication_date,publisher,total_count,available_count) )
            con.commit()
        flash("Book Added Successfully")
        return redirect('/books')
    return render_template('addbooks.html',title = 'Add Book',form = form)

@app.route('/deletebook/<string:id>',methods = ["GET","POST"])
def deletebook(id):
    flash("Book Deleted Successfully")
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM books WHERE bookID = ?",(id,) )
        con.commit()
    return redirect('/books')

@app.route('/editbook/<string:id>',methods = ["GET","POST"])
def editbook(id):

    form = BookForm()
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        book = cur.execute("SELECT * FROM books WHERE bookID = ?",(id,) ).fetchone()
        if(book):
            return render_template('editbook.html',form = form,book = book)


    if form.validate_on_submit():
        bookID = form.bookID.data
        title = form.title.data
        authors = form.authors.data
        average_rating = form.average_rating.data
        isbn = form.isbn.data
        isbn13 = form.isbn13.data
        language_code = form.language_code.data
        num_pages = form.num_pages.data
        ratings_count = form.ratings_count.data
        text_reviews_count = form.text_reviews_count.data
        publication_date = form.publication_date.data
        publisher = form.publisher.data
        total_count = form.total_count.data
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("UPDATE books SET title=?,authors=?,average_rating=?,isbn=?,isbn13=?,language_code=?,num_pages=?,ratings_count=?,text_reviews_count=?,publication_date=?,publisher=?,total_count=? WHERE bookID = ?",(title,authors,average_rating,isbn,isbn13,language_code,num_pages,ratings_count,text_reviews_count,publication_date,publisher,total_count,bookID) )
            con.commit()
        flash("Book Updated Successfully")
        return redirect('/books')

@app.route('/importbooks',methods = ["GET","POST"])
def importbooks():
    form = ImportForm()
    if form.validate_on_submit():
        title = form.title.data or ""
        author = form.authors.data or ""
        page = 1
        publisher = form.publisher.data or ""
        repeated_books = []
        no_of_books_imported = 0
        while(no_of_books_imported != form.number_of_books.data):
                url = 'https://frappe.io/api/method/frappe-library'
                payload = {"title":title,"author":author,"page":page,"publisher":publisher}
                res = requests.get(url,params=payload).json()
                if res['message']:
                    with sqlite3.connect('database.db') as con:
                        cur = con.cursor()
                    for book in res['message']:
                        cur.execute("SELECT bookID FROM books WHERE bookID=?", [book['bookID']])
                        book_found = cur.fetchone()
                        if not book_found:
                            bookID = book['bookID']
                            title = book['title']
                            authors = book['authors']
                            average_rating = book['average_rating']
                            isbn = book['isbn']
                            isbn13 = book['isbn13']
                            language_code = book['language_code']
                            num_pages = book['  num_pages']
                            ratings_count = book['ratings_count']
                            text_reviews_count = book['text_reviews_count']
                            publication_date = book['publication_date']
                            publisher = book['publisher']
                            total_count = form.quantity_per_book.data
                            available_count = form.quantity_per_book.data

                            cur.execute("INSERT INTO books (bookID,title,authors,average_rating,isbn,isbn13,language_code,num_pages,ratings_count,text_reviews_count,publication_date,publisher,total_count,available_count) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(bookID,title,authors,average_rating,isbn,isbn13,language_code,num_pages,ratings_count,text_reviews_count,publication_date,publisher,total_count,available_count) )
                                # con.commit()
                            no_of_books_imported+=1
                            if no_of_books_imported == form.number_of_books.data:
                                break
                        else:
                            repeated_books.append(book['bookID'])
                            print(repeated_books)

                payload["page"]+=1

        con.commit()
        con.close()
        
        flash("Books Added Successfully")
        return redirect('/books')
    return render_template('importbooks.html',title = 'Import Books',form = form)

    


@app.route('/members',methods = ["GET","POST"])
def members():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    # result = 
    members = cur.execute("SELECT * FROM members ORDER BY memberID").fetchall()
    cur.close()

    # Render Template
    if len(members) > 0:
        return render_template('members.html', members=members)
    else:
        msg = 'No Members Found'
        return render_template('members.html', members=members, msg=msg)

    # Close DB Connection

@app.route('/addmembers',methods = ["GET","POST"])
def addmember():
    form = MemberForm()
    if form.validate_on_submit():
        memberID = form.memberID.data
        name = form.name.data
        email = form.email.data
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO members (memberID,name,email) VALUES (?,?,?)",(memberID,name,email) )
            con.commit()
        flash("Member Added Successfully")
        return redirect('/members')
    return render_template('addmembers.html',title = 'Add Member',form = form)  

@app.route('/deletemember/<string:id>',methods = ["GET","POST"])
def deletemember(id):
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM members WHERE memberID = ?",(id,) )
        con.commit()
    flash("Member Deleted Successfully")
    return redirect('/members')

@app.route('/editmember/<string:id>',methods = ["GET","POST"])
def editmember(id):
    
        form = MemberForm()
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            member = cur.execute("SELECT * FROM members WHERE memberID = ?",(id,) ).fetchone()
            if(member):
                return render_template('editmember.html',form = form,member = member)
    
    
        if form.validate_on_submit():
            memberID = form.memberID.data
            name = form.name.data
            email = form.email.data
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE members SET name=?,email=? WHERE memberID = ?",(name,email,memberID) )
                con.commit()
            flash("Member Updated Successfully")
            return redirect('/members')

@app.route('/transactions',methods = ["GET","POST"])
def transactions():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    # result = 
    transactions = cur.execute("SELECT * FROM RENT").fetchall()
    cur.close()

    # Render Template
    if len(transactions) > 0:
        return render_template('transactions.html', transactions=transactions)
    else:
        msg = 'No Transactions Found'
        return render_template('transactions.html', transactions=transactions, msg=msg)

    # Close DB Connection

@app.route('/issuebooks',methods = ["GET","POST"])
def borrowbooks():
    form = IssueForm()
    if form.validate_on_submit():
        bookID = form.bookID.data
        memberID = form.memberID.data
        day_fee = form.day_fee.data
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            # cur.execute("INSERT INTO RENT (bookID,memberID,day_fee) VALUES (?,?,?)",(bookID,memberID,day_fee) )
            # cur.execute("UPDATE books SET total_count = total_count - 1 WHERE bookID = ?",(bookID,) )
            # # If table is empty set rentID to 1
            cur.execute("SELECT COUNT(*) FROM RENT")
            count = cur.fetchone()[0]
            if count == 0:
                rentID = 1
            else:
                cur.execute("SELECT MAX(rentID) FROM RENT")
                rentID = cur.fetchone()[0] + 1
            cur.execute("INSERT INTO RENT (rentID,bookID,memberID,day_fee) VALUES (?,?,?,?)",(rentID,bookID,memberID,day_fee) )
            cur.execute("UPDATE books SET available_count = available_count - 1, rent_count = rent_count + 1 WHERE bookID = ?",(bookID,))
            con.commit()
        flash("Book Borrowed Successfully")
        return redirect('/books')
    return render_template('issuebooks.html',title = 'Borrow Books',form = form)

@app.route('/returnbook/<string:id>',methods = ["GET","POST"])
def returnbook(id):
    form = ReturnForm()
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        transactions = cur.execute("SELECT * FROM RENT WHERE rentID = ?",(id,) ).fetchone()
        cur.execute("SELECT * FROM RENT WHERE rentID = ?",(id,) )
        rent = cur.fetchone()
        date = datetime.now()
        # print(date)
        # print(rent['rent_date'], flush=True)
        # difference = date - rent[6]
        difference = date - datetime.strptime(rent[6], '%Y-%m-%d')
        print(difference)
        sys.stdout.flush()
        days = difference.days
        total_fee = days * rent[3]
    
    if form.validate_on_submit():
        amount_paid = form.amount_paid.data
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM RENT WHERE rentID = ?",(id,) )
            rent = cur.fetchone()
            date = datetime.now()
            difference = date - datetime.strptime(rent[6], '%Y-%m-%d')
            print(difference)
            days = difference.days
            total_fee = days * rent[3]
            cur.execute("UPDATE RENT SET amount_paid = ?, return_date = ?, total_amount = ? WHERE rentID = ?",(amount_paid,date,total_fee,id) )
            cur.execute("UPDATE books SET available_count = available_count + 1 WHERE bookID = ?",(rent[2],) )
            con.commit()
        flash("Book Returned Successfully")
        return redirect('/transactions')
    return render_template('returnbook.html',title = 'Return Book',form = form, transactions=transactions, difference=difference, days=days, total_fee=total_fee)
            
@app.route('/reports',methods = ["GET","POST"])
def reports():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    # result = 
    expenses = cur.execute("SELECT SUM(amount_paid) AS AMOUNT,SUM(total_amount) AS TOTAL FROM RENT").fetchone()
    # Get members joined this month
    cur.execute("SELECT COUNT(*) FROM members WHERE strftime('%m', reg_date) = strftime('%m', 'now')")
    members_joined = cur.fetchone()[0]

    cur.close()



    return render_template('reports.html', expenses=expenses, members_joined=members_joined)


if __name__ == '__main__':
  app.run(debug=True)