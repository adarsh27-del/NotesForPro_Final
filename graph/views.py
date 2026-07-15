# graph/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
import json
import pandas as pd
from io import StringIO
import plotly.express as px
import plotly.graph_objects as go
from plotly.io import to_json
import traceback


@login_required
def graph_creator(request):
    """Main view - renders the graph creator page"""
    return render(request, 'graph/creator.html', {
        'page_title': 'Graph Creator – NotesForPro',
    })


@require_POST
@login_required
def graph_generate(request):
    """
    API endpoint to generate Plotly JSON from form data
    Supports: line, bar, scatter, pie, surface3d, scatter3d
    """
    try:
        # ─── Form fields ────────────────────────────────────────────────
        plot_type   = request.POST.get('plot_type',   'line')
        title       = request.POST.get('title',       'Untitled Chart')
        x_label     = request.POST.get('x_label',     'X Axis')
        y_label     = request.POST.get('y_label',     'Y Axis')
        show_legend = request.POST.get('show_legend', 'true').lower() == 'true'

        # ─── Read data ──────────────────────────────────────────────────
        df = None

        # Priority 1: uploaded file
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            content = csv_file.read().decode('utf-8')
            df = pd.read_csv(StringIO(content))

        # Priority 2: pasted text
        elif csv_text := request.POST.get('csv_text', '').strip():
            df = pd.read_csv(StringIO(csv_text))

        # Fallback: nice-looking dummy data (multi-series friendly)
        if df is None or df.empty:
            df = pd.DataFrame({
                'x':     [1, 2, 3, 4, 5, 6, 7],
                'y1':    [12, 18, 15, 22, 19, 25, 21],
                'y2':    [10, 14, 13, 20, 17, 23, 19],
                'group': ['A', 'A', 'B', 'B', 'C', 'C', 'A'],
                'z':     [3, 6, 4, 9, 5, 11, 7]
            })

        # ─── Common beautiful dark layout ───────────────────────────────
        common_layout = {
            'title': title,
            'xaxis_title': x_label,
            'yaxis_title': y_label,
            'template': 'plotly_dark',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(30,41,59,0.4)',
            'font': {'color': '#e0f0ff', 'size': 14},
            'margin': {'l': 70, 'r': 40, 't': 90, 'b': 70},
            'showlegend': show_legend,
            'legend': {
                'bgcolor': 'rgba(40,50,70,0.65)',
                'bordercolor': '#475569',
                'borderwidth': 1,
                'font': {'size': 13}
            },
            'hovermode': 'closest',
            'dragmode': 'zoom',
        }

        # ─── Generate figure based on type ──────────────────────────────
        fig = None

        if plot_type == 'line':
            fig = px.line(
                df, x='x', y=[col for col in df.columns if col.startswith('y')],
                color='group' if 'group' in df else None,
                title=title
            )

        elif plot_type == 'bar':
            fig = px.bar(
                df, x='x', y=[col for col in df.columns if col.startswith('y')],
                color='group' if 'group' in df else None,
                barmode='group',
                title=title
            )

        elif plot_type == 'scatter':
            fig = px.scatter(
                df, x='x', y='y1',
                color='group' if 'group' in df else None,
                size='z' if 'z' in df else None,
                title=title
            )

        elif plot_type == 'pie':
            # Use first numeric column as values, first categorical as names
            value_col = next((c for c in df.columns if df[c].dtype in ['float64', 'int64']), 'y1')
            name_col  = next((c for c in df.columns if df[c].dtype == 'object'), 'group')
            fig = px.pie(df, values=value_col, names=name_col, title=title)

        elif plot_type == 'surface3d':
            # Simple surface — assumes grid-like data or we sample
            if 'z' in df.columns:
                fig = go.Figure(data=[go.Surface(
                    z=df['z'],
                    x=df['x'],
                    y=df.get('y1', df['x'] * 0),  # fallback
                    colorscale='Viridis',
                    showscale=True
                )])
            else:
                # fake grid if no z
                x, y = df['x'], df.get('y1', df['x'])
                z = (x * y).values.reshape(-1, len(df)//3 or 1)
                fig = go.Figure(data=[go.Surface(z=z, colorscale='Plasma')])

            fig.update_layout(
                scene=dict(
                    xaxis_title=x_label,
                    yaxis_title=y_label,
                    zaxis_title='Z Value'
                ),
                **common_layout
            )

        elif plot_type == 'scatter3d':
            fig = px.scatter_3d(
                df, x='x', y='y1', z='z' if 'z' in df else df['x']*0 + 5,
                color='group' if 'group' in df else None,
                title=title
            )
            fig.update_layout(
                scene=dict(
                    xaxis_title=x_label,
                    yaxis_title=y_label,
                    zaxis_title='Z'
                ),
                **common_layout
            )

        else:
            # fallback to line
            fig = px.line(df, x='x', y='y1', title=title)

        # Apply common layout to all
        if fig is not None:
            fig.update_layout(**common_layout)

        return JsonResponse({
            'success': True,
            'graph_json': to_json(fig),
            'dataframe_preview': df.head(12).to_html(
                classes='min-w-full divide-y divide-gray-700 text-sm text-gray-300',
                index=False,
                border=0
            )
        })

    except pd.errors.ParserError as e:
        return JsonResponse({
            'success': False,
            'error': 'Invalid CSV format. Please check headers and data.'
        }, status=400)

    except Exception as e:
        # In development — show traceback
        return JsonResponse({
            'success': False,
            'error': str(e),
            'detail': traceback.format_exc() if settings.DEBUG else None
        }, status=400)