
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE

# Bokeh
from bokeh.io import show, output_file
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import HoverTool
import matplotlib as mpl
from IPython.display import display, HTML


def _plot_scatter(color_by, x_tsne):
    # sns settings
    sns.set(rc={'figure.figsize':(15,15)})
    # colors
    palette = sns.color_palette("bright", len(set(color_by)))
    # plot
    sns.scatterplot(x_tsne[:,0], x_tsne[:,1], hue=color_by, legend='full', palette=palette)
    plt.title("t-SNE K-means clusters")
    # plt.savefig("plots/plot.png")
    plt.show()

def plot_tsne(xtrain_ctv, ytrain, perplexity):
    '''
    ytrain: train labels
    xtrain_ctv: embedding matrix - train data
    perplexity: t-sne variable
    plots a t-SNE scatterplot
    '''
    tsne = TSNE(perplexity=perplexity, learning_rate=1000,
            early_exaggeration=8.0, n_iter=1000, random_state=0, metric='l2')
    x_tsne = tsne.fit_transform(xtrain_ctv)
    output_file('plot.html')
    source_train = ColumnDataSource(
            data=dict(
                x = x_tsne[:,0],
                y = x_tsne[:,1],
                desc = ytrain,
                colors = ["#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in
                          255*mpl.cm.jet(mpl.colors.Normalize()(ytrain))],
                coll_date = train_df['Collection_Date'],
                gb_title = train_df['GenBank_Title'],
                sp = train_df['Host']
            )
        )

    source_test = ColumnDataSource(
            data=dict(
                x = test_tsne[:,0],
                y = test_tsne[:,1],
                desc = ytest,
                coll_date = test_df['Collection_Date'],
                gb_title = test_df['GenBank_Title'],
                sp = test_df['Host']
            )
        )

    hover_tsne = HoverTool(names=["test", "train"], tooltips=[("Cluster", "@desc"),
                                     ("Collection date", "@coll_date"),
                                     ("Genbank_title", "@gb_title"),
                                     ("Host", "@sp")])
    tools_tsne = [hover_tsne, 'pan', 'wheel_zoom', 'reset', 'save']
    plot_tsne = figure(plot_width=600, plot_height=600, tools=tools_tsne, title='t-SNE orf1ab')
    plot_tsne.legend.location = "top_left"

    # plot_tsne.square('x', 'y', size=7, fill_color='orange',
    #                  alpha=0.9, line_width=0, source=source_test, name="test")
    plot_tsne.circle('x', 'y', size=10, fill_color='colors',
                     alpha=0.5, line_width=0, source=source_train, name="train", legend_field='desc')

    # show(plot_tsne)
    display(HTML('plot.html'))
